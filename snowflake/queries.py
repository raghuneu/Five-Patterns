"""
snowflake/queries.py
Core Snowflake + Cortex interface for Chapter 04 demos.

Provides seven classes that map 1-to-1 to the demo's infrastructure needs:

    SnowflakeConnection  — credential loading & connection management
    CortexLLM            — LLM calls via Cortex, with logging and fallback
    MemoryStore           — read/write/poison agent memory  (Pattern 5)
    AgentMessageBus       — inter-agent messaging & deadlock (Pattern 4)
    ReflectionLogger      — generate-critique round logging  (Pattern 3)
    PlanStore             — execution-plan storage & staleness (Pattern 2)
    PatternEvaluator      — cross-pattern recommendation & evaluation

Every SQL statement targets the tables created by snowflake/setup.sql.
"""

from __future__ import annotations

import os
import time
import uuid
from typing import Any

import pandas as pd
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()


# ---------------------------------------------------------------------------
# Custom exception
# ---------------------------------------------------------------------------

class DeadlockError(Exception):
    """Raised when two agents are waiting on each other and neither can proceed."""


# ═══════════════════════════════════════════════════════════════════════════
# 1. SnowflakeConnection
# ═══════════════════════════════════════════════════════════════════════════

class SnowflakeConnection:
    """Manages a single Snowflake connection backed by .env credentials.

    Usage::

        sf = SnowflakeConnection()
        conn = sf.connect()
        sf.test_connection()
        rows = sf.execute_query("SELECT 1 AS n")
        sf.close()
    """

    def __init__(self) -> None:
        """Load credentials from environment variables (via .env file)."""
        self.user: str = os.getenv("SNOWFLAKE_USER", "")
        self.password: str = os.getenv("SNOWFLAKE_PASSWORD", "")
        self.account: str = os.getenv("SNOWFLAKE_ACCOUNT", "")
        self.warehouse: str = os.getenv("SNOWFLAKE_WAREHOUSE", "AGENTIC_DEMO_WH")
        self.database: str = os.getenv("SNOWFLAKE_DATABASE", "AGENTIC_SYSTEMS_BOOK")
        self.schema: str = os.getenv("SNOWFLAKE_SCHEMA", "CHAPTER04")
        self._conn: snowflake.connector.SnowflakeConnection | None = None

    def connect(self) -> snowflake.connector.SnowflakeConnection:
        """Establish and return a Snowflake connection.

        If a connection is already open it is returned as-is.
        """
        if self._conn is None or self._conn.is_closed():
            self._conn = snowflake.connector.connect(
                user=self.user,
                password=self.password,
                account=self.account,
                warehouse=self.warehouse,
                database=self.database,
                schema=self.schema,
            )
        return self._conn

    def test_connection(self) -> str:
        """Run the Cortex verification query and print the result.

        Returns:
            The Cortex response string.
        """
        conn = self.connect()
        cur = conn.cursor(snowflake.connector.DictCursor)
        cur.execute(
            "SELECT SNOWFLAKE.CORTEX.COMPLETE("
            "  'mistral-large',"
            "  'Respond with exactly: Cortex connection verified.'"
            ") AS cortex_test"
        )
        row = cur.fetchone()
        result = row["CORTEX_TEST"] if row else ""
        print(f"Cortex test: {result}")
        return result

    def execute_query(
        self, sql: str, params: dict[str, Any] | None = None
    ) -> list[dict]:
        """Execute arbitrary SQL and return results as a list of dicts.

        Args:
            sql: The SQL statement to execute.
            params: Optional bind parameters (pyformat style).

        Returns:
            A list of row-dicts. Empty list for DML statements.
        """
        conn = self.connect()
        cur = conn.cursor(snowflake.connector.DictCursor)
        cur.execute(sql, params)
        return cur.fetchall()

    def close(self) -> None:
        """Close the underlying connection if open."""
        if self._conn is not None and not self._conn.is_closed():
            self._conn.close()
            self._conn = None


# ═══════════════════════════════════════════════════════════════════════════
# 2. CortexLLM
# ═══════════════════════════════════════════════════════════════════════════

class CortexLLM:
    """Interface to Snowflake Cortex COMPLETE with automatic call logging.

    Every call is timed and (optionally) persisted to the LLM_CALL_LOG table
    so that the notebook can later compare latency, token counts, and
    outputs across patterns and failure modes.

    Usage::

        llm = CortexLLM(sf)
        answer = llm.complete("Summarise X", pattern_name="reflection")
    """

    # Mock responses keyed by pattern_name prefix — used in offline / failure demos.
    _MOCK_RESPONSES: dict[str, str] = {
        "tool_use": (
            "I'll use the search tool to look up the current weather. "
            "[TOOL_CALL: search('current weather forecast')]"
        ),
        "planning": (
            "Step 1: Gather requirements\n"
            "Step 2: Design schema\n"
            "Step 3: Implement queries\n"
            "Step 4: Validate results"
        ),
        "reflection": (
            "Draft: The proposal addresses key stakeholder concerns. "
            "Critique: Needs stronger evidence in section 2. Score: 6/10."
        ),
        "multi_agent": (
            "Agent-Researcher: I found three relevant papers. "
            "Passing findings to Agent-Writer for synthesis."
        ),
        "memory": (
            "Retrieved from memory: User previously preferred concise "
            "bullet-point summaries. Applying that preference now."
        ),
        "scaffold": (
            "SYSTEM ANALYSIS\n"
            "Task: Multi-source research with synthesis and review\n\n"
            "PROPOSED AGENT ROLES:\n"
            "1. Researcher — queries external sources, returns structured findings\n"
            "2. Writer — synthesizes findings into coherent prose\n"
            "3. Reviewer — evaluates output against quality criteria\n\n"
            "PROPOSED TOOL DEFINITIONS:\n"
            "- search(query: str) -> str — web/database lookup\n"
            "- calculator(expr: str) -> float — arithmetic evaluation\n"
            "- formatter(text: str, style: str) -> str — output formatting\n\n"
            "RECOMMENDED PATTERN: Multi-Agent Collaboration\n"
            "REASONING: Task requires distinct specialization (research vs writing "
            "vs review). Single-agent ReAct would overload context. "
            "Plan-and-Execute lacks the feedback loop between writer and reviewer."
        ),
    }

    def __init__(
        self,
        sf: SnowflakeConnection,
        model: str = "mistral-large",
        log_calls: bool = True,
    ) -> None:
        """Initialise the LLM wrapper.

        Args:
            sf: An active SnowflakeConnection instance.
            model: Cortex model identifier (default ``mistral-large``).
            log_calls: Whether to persist every call to LLM_CALL_LOG.
        """
        self.sf = sf
        self.model = model
        self.log_calls = log_calls

    def complete(
        self,
        prompt: str,
        pattern_name: str,
        call_type: str = "working",
    ) -> str:
        """Call Cortex COMPLETE, measure latency, and optionally log the call.

        Args:
            prompt: The text prompt sent to the model.
            pattern_name: Which pattern demo this call belongs to.
            call_type: ``'working'`` for normal calls, ``'failure'`` for
                intentional failure-mode demonstrations.

        Returns:
            The model's response string.
        """
        sql = (
            "SELECT SNOWFLAKE.CORTEX.COMPLETE(%(model)s, %(prompt)s) "
            "AS response"
        )

        start = time.time()
        rows = self.sf.execute_query(sql, {"model": self.model, "prompt": prompt})
        latency_ms = (time.time() - start) * 1000

        response = rows[0]["RESPONSE"] if rows else ""

        if self.log_calls:
            self._log(pattern_name, call_type, prompt, response, latency_ms)

        return response

    def complete_with_fallback(
        self,
        prompt: str,
        pattern_name: str,
        call_type: str = "working",
    ) -> str:
        """Try a live Cortex call; fall back to mock_llm on failure.

        Prints which mode is active so the notebook reader can tell at a
        glance whether they are seeing real or simulated output.

        Args:
            prompt: The text prompt.
            pattern_name: Pattern demo name.
            call_type: ``'working'`` or ``'failure'``.

        Returns:
            Response string (live or mocked).
        """
        try:
            result = self.complete(prompt, pattern_name, call_type)
            print(f"[CortexLLM] LIVE response from {self.model}")
            return result
        except Exception as exc:
            print(f"[CortexLLM] Cortex unavailable ({exc}). Using MOCK mode.")
            return self.mock_llm(prompt, pattern_name)

    def get_call_history(self, pattern_name: str | None = None) -> pd.DataFrame:
        """Query the LLM_CALL_LOG table and return results as a DataFrame.

        Args:
            pattern_name: If provided, filter to calls from this pattern only.

        Returns:
            A pandas DataFrame with all matching call records.
        """
        if pattern_name:
            sql = (
                "SELECT * FROM CHAPTER04.LLM_CALL_LOG "
                "WHERE pattern_name = %(pattern_name)s "
                "ORDER BY created_at"
            )
            rows = self.sf.execute_query(sql, {"pattern_name": pattern_name})
        else:
            sql = "SELECT * FROM CHAPTER04.LLM_CALL_LOG ORDER BY created_at"
            rows = self.sf.execute_query(sql)
        return pd.DataFrame(rows)

    def mock_llm(self, prompt: str, pattern_name: str = "tool_use") -> str:
        """Return a realistic hardcoded response for offline / failure demos.

        The response is chosen by *pattern_name*. If the pattern is not
        recognised, a generic acknowledgement is returned.

        Args:
            prompt: The prompt (logged but not used to select the response).
            pattern_name: Determines which canned response is returned.

        Returns:
            A mock response string.
        """
        response = self._MOCK_RESPONSES.get(
            pattern_name,
            f"[MOCK] Acknowledged prompt ({len(prompt)} chars). "
            "No live model available.",
        )

        if self.log_calls:
            self._log(pattern_name, "mock", prompt, response, 0.0)

        return response

    # -- internal helpers ---------------------------------------------------

    def _log(
        self,
        pattern_name: str,
        call_type: str,
        prompt: str,
        response: str,
        latency_ms: float,
    ) -> None:
        """Insert a record into LLM_CALL_LOG."""
        sql = (
            "INSERT INTO CHAPTER04.LLM_CALL_LOG "
            "(pattern_name, call_type, prompt, response, model_used, "
            " tokens_used, latency_ms) "
            "VALUES (%(pattern_name)s, %(call_type)s, %(prompt)s, "
            "%(response)s, %(model_used)s, %(tokens_used)s, %(latency_ms)s)"
        )
        # Rough token estimate: 1 token ≈ 4 characters
        tokens_est = (len(prompt) + len(response)) // 4
        try:
            self.sf.execute_query(sql, {
                "pattern_name": pattern_name,
                "call_type": call_type,
                "prompt": prompt,
                "response": response,
                "model_used": self.model,
                "tokens_used": tokens_est,
                "latency_ms": latency_ms,
            })
        except Exception:
            # Logging should never break the demo.
            pass


# ═══════════════════════════════════════════════════════════════════════════
# 3. MemoryStore  (Pattern 5 — Memory-Augmented Agent)
# ═══════════════════════════════════════════════════════════════════════════

class MemoryStore:
    """Read, write, and deliberately corrupt agent memories in AGENT_MEMORY.

    Supports Pattern 5's working demo (keyword-based retrieval of short-
    and long-term memory) and its failure mode (memory poisoning).

    Usage::

        mem = MemoryStore(sf, session_id="demo-001")
        mem.write_memory("User prefers bullet points", "long_term", "preferences")
        results = mem.retrieve_memory("preferences")
    """

    def __init__(self, sf: SnowflakeConnection, session_id: str) -> None:
        """Initialise the store for a given session.

        Args:
            sf: An active SnowflakeConnection instance.
            session_id: Groups memories belonging to one demo run.
        """
        self.sf = sf
        self.session_id = session_id

    def write_memory(
        self,
        content: str,
        memory_type: str,
        embedding_text: str,
        is_poisoned: bool = False,
    ) -> str:
        """Insert a new memory record.

        Args:
            content: The memory content.
            memory_type: ``'short_term'`` or ``'long_term'``.
            embedding_text: Simplified keyword string for retrieval.
            is_poisoned: Mark this memory as deliberately corrupted.

        Returns:
            The generated memory_id.
        """
        memory_id = str(uuid.uuid4())
        sql = (
            "INSERT INTO CHAPTER04.AGENT_MEMORY "
            "(memory_id, session_id, memory_type, content, "
            " embedding_text, is_poisoned) "
            "VALUES (%(memory_id)s, %(session_id)s, %(memory_type)s, "
            "%(content)s, %(embedding_text)s, %(is_poisoned)s)"
        )
        self.sf.execute_query(sql, {
            "memory_id": memory_id,
            "session_id": self.session_id,
            "memory_type": memory_type,
            "content": content,
            "embedding_text": embedding_text,
            "is_poisoned": is_poisoned,
        })
        return memory_id

    def retrieve_memory(
        self, query_keyword: str, memory_type: str | None = None
    ) -> list[dict]:
        """Retrieve memories whose embedding_text contains the keyword.

        Args:
            query_keyword: Substring to match against embedding_text.
            memory_type: Optional filter (``'short_term'`` / ``'long_term'``).

        Returns:
            A list of matching memory row dicts.
        """
        if memory_type:
            sql = (
                "SELECT * FROM CHAPTER04.AGENT_MEMORY "
                "WHERE session_id = %(session_id)s "
                "  AND LOWER(embedding_text) LIKE %(kw)s "
                "  AND memory_type = %(memory_type)s "
                "ORDER BY created_at"
            )
            params = {
                "session_id": self.session_id,
                "kw": f"%{query_keyword.lower()}%",
                "memory_type": memory_type,
            }
        else:
            sql = (
                "SELECT * FROM CHAPTER04.AGENT_MEMORY "
                "WHERE session_id = %(session_id)s "
                "  AND LOWER(embedding_text) LIKE %(kw)s "
                "ORDER BY created_at"
            )
            params = {
                "session_id": self.session_id,
                "kw": f"%{query_keyword.lower()}%",
            }
        return self.sf.execute_query(sql, params)

    def poison_memory(self, memory_id: str, false_content: str) -> None:
        """Overwrite a memory with false content and flag it as poisoned.

        This is the **deliberate failure trigger** for Pattern 5.  The
        agent will later retrieve this corrupted memory and produce a
        degraded response, demonstrating the risk of unbounded memory trust.

        Args:
            memory_id: The ID of the memory to corrupt.
            false_content: The misleading content to inject.
        """
        sql = (
            "UPDATE CHAPTER04.AGENT_MEMORY "
            "SET content = %(content)s, is_poisoned = TRUE "
            "WHERE memory_id = %(memory_id)s"
        )
        self.sf.execute_query(sql, {
            "content": false_content,
            "memory_id": memory_id,
        })

    def clear_session(self, session_id: str | None = None) -> None:
        """Delete all memories for a session.

        Args:
            session_id: Session to clear. Defaults to this store's session.
        """
        sid = session_id or self.session_id
        sql = (
            "DELETE FROM CHAPTER04.AGENT_MEMORY "
            "WHERE session_id = %(session_id)s"
        )
        self.sf.execute_query(sql, {"session_id": sid})


# ═══════════════════════════════════════════════════════════════════════════
# 4. AgentMessageBus  (Pattern 4 — Multi-Agent Coordination)
# ═══════════════════════════════════════════════════════════════════════════

class AgentMessageBus:
    """Inter-agent message passing backed by the AGENT_MESSAGES table.

    Supports the working demo (send → poll → deliver) and the failure mode
    (circular-wait deadlock between two agents).

    Usage::

        bus = AgentMessageBus(sf, session_id="demo-004")
        bus.send_message("researcher", "writer", "Here are the facts.")
        msg = bus.receive_message("writer")
    """

    def __init__(self, sf: SnowflakeConnection, session_id: str) -> None:
        """Initialise the bus for a given session.

        Args:
            sf: An active SnowflakeConnection instance.
            session_id: Groups messages belonging to one demo run.
        """
        self.sf = sf
        self.session_id = session_id

    def send_message(
        self, from_agent: str, to_agent: str, content: str
    ) -> str:
        """Insert a pending message from one agent to another.

        Args:
            from_agent: Sender agent name.
            to_agent: Recipient agent name.
            content: Message body.

        Returns:
            The generated message_id.
        """
        message_id = str(uuid.uuid4())
        sql = (
            "INSERT INTO CHAPTER04.AGENT_MESSAGES "
            "(message_id, session_id, from_agent, to_agent, "
            " message_content, status) "
            "VALUES (%(message_id)s, %(session_id)s, %(from_agent)s, "
            "%(to_agent)s, %(content)s, 'pending')"
        )
        self.sf.execute_query(sql, {
            "message_id": message_id,
            "session_id": self.session_id,
            "from_agent": from_agent,
            "to_agent": to_agent,
            "content": content,
        })
        return message_id

    def receive_message(
        self, agent_name: str, timeout_seconds: float = 5.0
    ) -> dict:
        """Poll for a pending message addressed to *agent_name*.

        Polls once per second up to *timeout_seconds*.  On success the
        message status is updated to ``'delivered'``.

        Args:
            agent_name: The agent waiting for a message.
            timeout_seconds: How long to poll before raising DeadlockError.

        Returns:
            The message row dict.

        Raises:
            DeadlockError: If no message arrives within the timeout.
        """
        sql = (
            "SELECT * FROM CHAPTER04.AGENT_MESSAGES "
            "WHERE session_id = %(session_id)s "
            "  AND to_agent = %(agent)s "
            "  AND status = 'pending' "
            "ORDER BY created_at LIMIT 1"
        )
        deadline = time.time() + timeout_seconds
        while time.time() < deadline:
            rows = self.sf.execute_query(
                sql, {"session_id": self.session_id, "agent": agent_name}
            )
            if rows:
                msg = rows[0]
                self._mark_delivered(msg["MESSAGE_ID"])
                return msg
            time.sleep(1)

        raise DeadlockError(
            f"Agent '{agent_name}' received no message within "
            f"{timeout_seconds}s — possible deadlock."
        )

    def create_deadlock(self, agent_a: str, agent_b: str) -> None:
        """Simulate a circular-wait deadlock between two agents.

        Both agents are made to wait for the other, with no pending
        messages from either side.  All their existing pending messages
        are marked ``'deadlocked'``.

        This is the **deliberate failure trigger** for Pattern 4.

        Args:
            agent_a: First agent in the deadlock pair.
            agent_b: Second agent in the deadlock pair.
        """
        sql = (
            "UPDATE CHAPTER04.AGENT_MESSAGES "
            "SET status = 'deadlocked' "
            "WHERE session_id = %(session_id)s "
            "  AND status = 'pending' "
            "  AND ((from_agent = %(a)s AND to_agent = %(b)s) "
            "    OR (from_agent = %(b)s AND to_agent = %(a)s))"
        )
        self.sf.execute_query(sql, {
            "session_id": self.session_id,
            "a": agent_a,
            "b": agent_b,
        })
        print(
            f"[AgentMessageBus] Deadlock injected between "
            f"'{agent_a}' and '{agent_b}'."
        )

    # -- internal helpers ---------------------------------------------------

    def _mark_delivered(self, message_id: str) -> None:
        """Update a message's status to 'delivered'."""
        sql = (
            "UPDATE CHAPTER04.AGENT_MESSAGES "
            "SET status = 'delivered' "
            "WHERE message_id = %(mid)s"
        )
        self.sf.execute_query(sql, {"mid": message_id})


# ═══════════════════════════════════════════════════════════════════════════
# 5. ReflectionLogger  (Pattern 3 — Self-Reflection / Critic Loop)
# ═══════════════════════════════════════════════════════════════════════════

class ReflectionLogger:
    """Logs generate-critique rounds to REFLECTION_ROUNDS.

    Each row captures one iteration of the reflection loop: what the
    generator produced, how the critic scored it, and whether the loop
    converged.

    Usage::

        rl = ReflectionLogger(sf, session_id="demo-003")
        rl.log_round(1, "Draft v1...", 4.5, "Needs more evidence", False)
    """

    def __init__(self, sf: SnowflakeConnection, session_id: str) -> None:
        """Initialise the logger for a given session.

        Args:
            sf: An active SnowflakeConnection instance.
            session_id: Groups rounds belonging to one demo run.
        """
        self.sf = sf
        self.session_id = session_id

    def log_round(
        self,
        round_number: int,
        output: str,
        score: float,
        feedback: str,
        converged: bool,
    ) -> str:
        """Insert one reflection round.

        Args:
            round_number: 1-based iteration count.
            output: The generator's output for this round.
            score: The critic's numeric score.
            feedback: The critic's textual feedback.
            converged: Whether the critic accepted the output.

        Returns:
            The generated round_id.
        """
        round_id = str(uuid.uuid4())
        sql = (
            "INSERT INTO CHAPTER04.REFLECTION_ROUNDS "
            "(round_id, session_id, round_number, generated_output, "
            " critic_score, critic_feedback, converged) "
            "VALUES (%(round_id)s, %(session_id)s, %(round_number)s, "
            "%(output)s, %(score)s, %(feedback)s, %(converged)s)"
        )
        self.sf.execute_query(sql, {
            "round_id": round_id,
            "session_id": self.session_id,
            "round_number": round_number,
            "output": output,
            "score": score,
            "feedback": feedback,
            "converged": converged,
        })
        return round_id

    def get_convergence_data(self, session_id: str | None = None) -> pd.DataFrame:
        """Return all reflection rounds for a session as a DataFrame.

        Useful for plotting score trajectories and identifying
        non-convergence in the failure demo.

        Args:
            session_id: Session to query. Defaults to this logger's session.

        Returns:
            A pandas DataFrame ordered by round_number.
        """
        sid = session_id or self.session_id
        sql = (
            "SELECT * FROM CHAPTER04.REFLECTION_ROUNDS "
            "WHERE session_id = %(session_id)s "
            "ORDER BY round_number"
        )
        rows = self.sf.execute_query(sql, {"session_id": sid})
        return pd.DataFrame(rows)


# ═══════════════════════════════════════════════════════════════════════════
# 6. PlanStore  (Pattern 2 — Planning / Re-planning Agent)
# ═══════════════════════════════════════════════════════════════════════════

class PlanStore:
    """Stores multi-step execution plans in EXECUTION_PLANS.

    Supports Pattern 2's working demo (sequential plan execution with
    world-state tracking) and its failure mode (stale-plan injection).

    Usage::

        ps = PlanStore(sf, session_id="demo-002")
        ps.store_plan(["Gather data", "Analyse", "Report"])
        ps.execute_step(1, "Gathered 50 rows", '{"rows": 50}')
    """

    def __init__(self, sf: SnowflakeConnection, session_id: str) -> None:
        """Initialise the store for a given session.

        Args:
            sf: An active SnowflakeConnection instance.
            session_id: Groups plan steps belonging to one demo run.
        """
        self.sf = sf
        self.session_id = session_id

    def store_plan(self, steps: list[str]) -> list[str]:
        """Insert a multi-step plan (one row per step).

        Args:
            steps: Ordered list of step descriptions.

        Returns:
            List of generated plan_id values.
        """
        sql = (
            "INSERT INTO CHAPTER04.EXECUTION_PLANS "
            "(plan_id, session_id, step_number, step_description) "
            "VALUES (%(plan_id)s, %(session_id)s, %(step_number)s, "
            "%(step_description)s)"
        )
        ids = []
        for i, desc in enumerate(steps, start=1):
            plan_id = str(uuid.uuid4())
            self.sf.execute_query(sql, {
                "plan_id": plan_id,
                "session_id": self.session_id,
                "step_number": i,
                "step_description": desc,
            })
            ids.append(plan_id)
        return ids

    def execute_step(
        self, step_number: int, result: str, world_state: str
    ) -> None:
        """Record the result and world state for a completed step.

        Args:
            step_number: The 1-based step index.
            result: What happened when this step ran.
            world_state: JSON snapshot of the world after execution.
        """
        sql = (
            "UPDATE CHAPTER04.EXECUTION_PLANS "
            "SET execution_result = %(result)s, "
            "    world_state_snapshot = %(world_state)s "
            "WHERE session_id = %(session_id)s "
            "  AND step_number = %(step_number)s"
        )
        self.sf.execute_query(sql, {
            "result": result,
            "world_state": world_state,
            "session_id": self.session_id,
            "step_number": step_number,
        })

    def inject_world_state_change(self, step_number: int) -> None:
        """Mark a step as stale by injecting a contradictory world state.

        This is the **deliberate failure trigger** for Pattern 2.  The
        agent's plan was built for one world state, but the world has
        changed underneath it — continuing to execute becomes unsafe.

        Args:
            step_number: The step whose world state should be corrupted.
        """
        sql = (
            "UPDATE CHAPTER04.EXECUTION_PLANS "
            "SET is_stale = TRUE, "
            "    world_state_snapshot = "
            "      '{\"injected\": true, \"reason\": \"world state changed\"}' "
            "WHERE session_id = %(session_id)s "
            "  AND step_number = %(step_number)s"
        )
        self.sf.execute_query(sql, {
            "session_id": self.session_id,
            "step_number": step_number,
        })
        print(
            f"[PlanStore] Step {step_number} marked stale — "
            "world state contradicts the original plan."
        )


# ═══════════════════════════════════════════════════════════════════════════
# 7. PatternEvaluator
# ═══════════════════════════════════════════════════════════════════════════

class PatternEvaluator:
    """Recommends patterns and logs evaluation outcomes to PATTERN_EVALUATIONS.

    Provides a simple decision tree that maps task characteristics to the
    most appropriate agentic pattern, plus CRUD for the evaluation table.

    Usage::

        ev = PatternEvaluator(sf)
        rec = ev.recommend_pattern(
            task_is_decomposable=True,
            needs_reflection=False,
            multiple_agents=False,
            stateful=False,
            iterative_tools=True,
        )
        print(rec)  # {'pattern': 'tool_use', 'reasoning': '...'}
    """

    _PATTERNS = {
        "tool_use": "Pattern 1 — Tool Use (Augmented LLM)",
        "planning": "Pattern 2 — Planning / Re-planning Agent",
        "reflection": "Pattern 3 — Self-Reflection / Critic Loop",
        "multi_agent": "Pattern 4 — Multi-Agent Coordination",
        "memory": "Pattern 5 — Memory-Augmented Agent",
    }

    def __init__(self, sf: SnowflakeConnection) -> None:
        """Initialise the evaluator.

        Args:
            sf: An active SnowflakeConnection instance.
        """
        self.sf = sf

    def recommend_pattern(
        self,
        task_is_decomposable: bool = False,
        needs_reflection: bool = False,
        multiple_agents: bool = False,
        stateful: bool = False,
        iterative_tools: bool = False,
    ) -> dict[str, str]:
        """Return the recommended pattern and reasoning for a task.

        The decision tree evaluates characteristics in order of
        specificity: multi-agent → stateful → reflection → decomposable
        → tool-use fallback.

        Args:
            task_is_decomposable: Can the task be broken into ordered steps?
            needs_reflection: Does output quality improve with self-critique?
            multiple_agents: Does the task need distinct agent roles?
            stateful: Must the agent remember across turns or sessions?
            iterative_tools: Does the task require external tool calls?

        Returns:
            A dict with ``'pattern'`` and ``'reasoning'`` keys.
        """
        if multiple_agents:
            return {
                "pattern": "multi_agent",
                "reasoning": (
                    "Task requires distinct agent roles collaborating. "
                    "Use multi-agent coordination with clear message passing."
                ),
            }
        if stateful:
            return {
                "pattern": "memory",
                "reasoning": (
                    "Task requires recall of prior context or user preferences. "
                    "Use a memory-augmented agent with retrieval."
                ),
            }
        if needs_reflection:
            return {
                "pattern": "reflection",
                "reasoning": (
                    "Output quality benefits from iterative self-critique. "
                    "Use a generator-critic loop with convergence criteria."
                ),
            }
        if task_is_decomposable:
            return {
                "pattern": "planning",
                "reasoning": (
                    "Task can be decomposed into sequential steps. "
                    "Use a planning agent that tracks world-state per step."
                ),
            }
        return {
            "pattern": "tool_use",
            "reasoning": (
                "Task is a single-shot request that may require external "
                "tools. Use an augmented LLM with tool-call capabilities."
            ),
        }

    def log_evaluation(
        self,
        pattern_name: str,
        task: str,
        was_correct: bool,
        failure_triggered: bool,
        failure_description: str = "",
        lesson: str = "",
    ) -> str:
        """Insert an evaluation record.

        Args:
            pattern_name: The pattern that was used.
            task: Description of the task.
            was_correct: Was this pattern the right choice?
            failure_triggered: Did the intentional failure mode fire?
            failure_description: What went wrong (if anything).
            lesson: Key architectural lesson learned.

        Returns:
            The generated eval_id.
        """
        eval_id = str(uuid.uuid4())
        sql = (
            "INSERT INTO CHAPTER04.PATTERN_EVALUATIONS "
            "(eval_id, pattern_name, task_description, was_correct_choice, "
            " failure_triggered, failure_description, architectural_lesson) "
            "VALUES (%(eval_id)s, %(pattern_name)s, %(task)s, "
            "%(was_correct)s, %(failure_triggered)s, "
            "%(failure_description)s, %(lesson)s)"
        )
        self.sf.execute_query(sql, {
            "eval_id": eval_id,
            "pattern_name": pattern_name,
            "task": task,
            "was_correct": was_correct,
            "failure_triggered": failure_triggered,
            "failure_description": failure_description,
            "lesson": lesson,
        })
        return eval_id

    def get_summary(self) -> pd.DataFrame:
        """Query all evaluation records and return them as a DataFrame.

        Returns:
            A pandas DataFrame with one row per evaluation, ordered by
            creation time.
        """
        sql = (
            "SELECT * FROM CHAPTER04.PATTERN_EVALUATIONS "
            "ORDER BY created_at"
        )
        rows = self.sf.execute_query(sql)
        return pd.DataFrame(rows)


# ═══════════════════════════════════════════════════════════════════════════
# Example usage
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("Chapter 04 — queries.py smoke test")
    print("=" * 60)

    # 1. Connect
    sf = SnowflakeConnection()
    print("\n[1] Connecting to Snowflake...")
    sf.connect()
    print("    Connected.")

    # 2. Test Cortex
    print("\n[2] Testing Cortex access...")
    sf.test_connection()

    # 3. CortexLLM — live call
    print("\n[3] CortexLLM.complete()...")
    llm = CortexLLM(sf)
    answer = llm.complete_with_fallback(
        "What is prompt engineering in one sentence?",
        pattern_name="tool_use",
    )
    print(f"    Response: {answer[:120]}...")

    # 4. MemoryStore — write and retrieve
    print("\n[4] MemoryStore — write / retrieve...")
    mem = MemoryStore(sf, session_id="smoke-test")
    mid = mem.write_memory(
        "User prefers concise answers",
        memory_type="long_term",
        embedding_text="preferences style concise",
    )
    results = mem.retrieve_memory("preferences")
    print(f"    Stored memory {mid}, retrieved {len(results)} result(s).")
    mem.clear_session("smoke-test")

    # 5. ReflectionLogger — log one round
    print("\n[5] ReflectionLogger — log round...")
    rl = ReflectionLogger(sf, session_id="smoke-test")
    rl.log_round(1, "Draft output", 7.0, "Solid start", False)
    df = rl.get_convergence_data()
    print(f"    Logged 1 round, got {len(df)} row(s) back.")

    # 6. PlanStore — store and execute
    print("\n[6] PlanStore — store plan...")
    ps = PlanStore(sf, session_id="smoke-test")
    ps.store_plan(["Gather data", "Analyse", "Report"])
    ps.execute_step(1, "Gathered 50 rows", '{"rows": 50}')
    print("    Stored 3-step plan, executed step 1.")

    # 7. PatternEvaluator — recommend
    print("\n[7] PatternEvaluator — recommend...")
    ev = PatternEvaluator(sf)
    rec = ev.recommend_pattern(needs_reflection=True)
    print(f"    Recommended: {rec['pattern']}")
    print(f"    Reasoning:   {rec['reasoning']}")

    # 8. Call history
    print("\n[8] LLM call history...")
    history = llm.get_call_history()
    print(f"    Total logged calls: {len(history)}")

    # Cleanup
    sf.close()
    print("\n" + "=" * 60)
    print("Smoke test complete.")
    print("=" * 60)
