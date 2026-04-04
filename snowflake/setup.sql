-- ============================================================================
-- AGENTIC SYSTEMS BOOK — Chapter 04: Five Agentic Patterns
-- Snowflake Setup Script
--
-- This script provisions the database, schema, warehouse, and all tables
-- needed to run the five agentic pattern demos. Each table captures a
-- specific aspect of agent behaviour so the demos can log, replay, and
-- analyse every step.
--
-- Run once before starting the demos. Safe to re-run (all objects use
-- IF NOT EXISTS).
-- ============================================================================

-- ---------------------------------------------------------------------------
-- 1. DATABASE
--    Top-level container for all demo artifacts.
-- ---------------------------------------------------------------------------
CREATE DATABASE IF NOT EXISTS AGENTIC_SYSTEMS_BOOK;

-- ---------------------------------------------------------------------------
-- 2. SCHEMA
--    Chapter-level namespace. Keeps Chapter 04 tables isolated from any
--    future chapters that may share the same database.
-- ---------------------------------------------------------------------------
CREATE SCHEMA IF NOT EXISTS AGENTIC_SYSTEMS_BOOK.CHAPTER04;

-- ---------------------------------------------------------------------------
-- 3. WAREHOUSE
--    A minimal X-Small warehouse dedicated to the demos. Auto-suspends
--    after 60 seconds of idle time to avoid unnecessary credit burn.
-- ---------------------------------------------------------------------------
CREATE WAREHOUSE IF NOT EXISTS AGENTIC_DEMO_WH
    WITH WAREHOUSE_SIZE = 'X-SMALL'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE;

-- Activate the warehouse, database, and schema for the rest of the script.
USE WAREHOUSE AGENTIC_DEMO_WH;
USE DATABASE AGENTIC_SYSTEMS_BOOK;
USE SCHEMA CHAPTER04;

-- ---------------------------------------------------------------------------
-- 4. TABLES
-- ---------------------------------------------------------------------------

-- LLM_CALL_LOG
-- Full audit trail of every LLM invocation made during any demo run.
-- Records both successful ("working") calls and intentional failure-mode
-- calls so readers can compare token usage, latency, and output quality
-- across patterns and failure scenarios.
CREATE TABLE IF NOT EXISTS CHAPTER04.LLM_CALL_LOG (
    call_id          VARCHAR   DEFAULT UUID_STRING(),
    pattern_name     VARCHAR,                          -- e.g. 'reflection', 'planning'
    call_type        VARCHAR,                          -- 'working' or 'failure'
    prompt           TEXT,
    response         TEXT,
    model_used       VARCHAR,
    tokens_used      INT,
    latency_ms       FLOAT,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- AGENT_MEMORY
-- Backs Pattern 5 (Memory-Augmented Agent). Stores both short-term
-- (within-session) and long-term (cross-session) memories. The
-- embedding_text column holds a simplified keyword representation
-- used for retrieval. The is_poisoned flag supports the failure-mode
-- demo where corrupted memories degrade agent performance.
CREATE TABLE IF NOT EXISTS CHAPTER04.AGENT_MEMORY (
    memory_id        VARCHAR   DEFAULT UUID_STRING(),
    session_id       VARCHAR,
    memory_type      VARCHAR,                          -- 'short_term' or 'long_term'
    content          TEXT,
    embedding_text   TEXT,                              -- simplified keyword for retrieval
    is_poisoned      BOOLEAN   DEFAULT FALSE,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- AGENT_MESSAGES
-- Backs Pattern 4 (Multi-Agent Coordination). Each row is a message
-- passed between agents within a session. The status column tracks
-- delivery state: 'pending' → 'delivered', or 'deadlocked' when the
-- failure-mode demo triggers a circular-wait condition.
CREATE TABLE IF NOT EXISTS CHAPTER04.AGENT_MESSAGES (
    message_id       VARCHAR   DEFAULT UUID_STRING(),
    session_id       VARCHAR,
    from_agent       VARCHAR,
    to_agent         VARCHAR,
    message_content  TEXT,
    status           VARCHAR   DEFAULT 'pending',      -- pending / delivered / deadlocked
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- REFLECTION_ROUNDS
-- Backs Pattern 3 (Self-Reflection / Critic Loop). Each row captures
-- one generate→critique round: the output produced, the critic's
-- numeric score and textual feedback, and whether the loop converged
-- (critic accepted the output). Allows post-hoc analysis of how many
-- rounds each task needed and where convergence stalled.
CREATE TABLE IF NOT EXISTS CHAPTER04.REFLECTION_ROUNDS (
    round_id         VARCHAR   DEFAULT UUID_STRING(),
    session_id       VARCHAR,
    round_number     INT,
    generated_output TEXT,
    critic_score     FLOAT,
    critic_feedback  TEXT,
    converged        BOOLEAN   DEFAULT FALSE,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- EXECUTION_PLANS
-- Backs Pattern 2 (Planning / Re-planning Agent). Stores the step-by-
-- step plan the agent builds, along with a world-state snapshot at each
-- step so the re-planner can detect drift. The is_stale flag marks
-- steps that were invalidated after the world state changed, which is
-- central to the failure-mode demo (stale-plan execution).
CREATE TABLE IF NOT EXISTS CHAPTER04.EXECUTION_PLANS (
    plan_id            VARCHAR   DEFAULT UUID_STRING(),
    session_id         VARCHAR,
    step_number        INT,
    step_description   TEXT,
    world_state_snapshot TEXT,
    execution_result   TEXT,
    is_stale           BOOLEAN   DEFAULT FALSE,
    created_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- PATTERN_EVALUATIONS
-- Cross-cutting evaluation table. After each demo run, a summary row
-- is written here recording which pattern was used, whether it was the
-- right architectural choice for the task, whether the failure mode
-- was triggered, and the key lesson learned. Powers the comparative
-- analysis at the end of the chapter.
CREATE TABLE IF NOT EXISTS CHAPTER04.PATTERN_EVALUATIONS (
    eval_id              VARCHAR   DEFAULT UUID_STRING(),
    pattern_name         VARCHAR,
    task_description     TEXT,
    was_correct_choice   BOOLEAN,
    failure_triggered    BOOLEAN,
    failure_description  TEXT,
    architectural_lesson TEXT,
    created_at           TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- ---------------------------------------------------------------------------
-- 5. VERIFY CORTEX ACCESS
--    Quick smoke test to confirm Snowflake Cortex LLM functions are
--    reachable from this account. If this returns a response, the demos
--    can safely call SNOWFLAKE.CORTEX.COMPLETE().
-- ---------------------------------------------------------------------------
SELECT SNOWFLAKE.CORTEX.COMPLETE(
    'mistral-large',
    'Respond with exactly: Cortex connection verified.'
) AS cortex_test;
