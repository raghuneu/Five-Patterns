# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

An interactive textbook chapter (*Agentic Systems*, Chapter 4: "Five Patterns, Five Trade-offs") demonstrating five agentic design patterns, each with a working implementation, a deliberate failure mode, and a mandatory human decision checkpoint. The central thesis: **architecture is the leverage point, not the model** — each pattern has a predictable failure mode that emerges from its design.

## Running the Demos

```bash
# Install dependencies
pip install snowflake-connector-python python-dotenv pandas matplotlib

# Launch notebook
jupyter notebook notebook/chapter04_demo.ipynb
```

**Before running the notebook**, execute `snowflake/setup.sql` in a Snowflake worksheet to create all infrastructure (database, schema, warehouse, 6 tables).

**Smoke test** the infrastructure classes without launching the notebook:
```bash
python snowflake/queries.py
```

**Teardown** (clean slate):
```sql
-- Execute snowflake/teardown.sql in a Snowflake worksheet
```

## Infrastructure

Credentials live in `.env` (gitignored). Required keys:
```
SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER, SNOWFLAKE_PASSWORD,
SNOWFLAKE_WAREHOUSE, SNOWFLAKE_DATABASE, SNOWFLAKE_SCHEMA, CORTEX_MODEL
```

`snowflake/setup.sql` creates `AGENTIC_SYSTEMS_BOOK.CHAPTER04` with six tables:

| Table | Used By |
|-------|---------|
| LLM_CALL_LOG | All patterns (every Cortex call logged) |
| EXECUTION_PLANS | Pattern 2 |
| REFLECTION_ROUNDS | Pattern 3 |
| AGENT_MESSAGES | Pattern 4 |
| AGENT_MEMORY | Pattern 5 |
| PATTERN_EVALUATIONS | Cross-pattern recommender |

## Code Architecture (`snowflake/queries.py`)

Seven classes; each pattern's infrastructure class exposes both working methods and explicit failure triggers:

| Class | Role | Failure Trigger Method |
|-------|------|----------------------|
| `SnowflakeConnection` | Credential loading, connection pooling | — |
| `CortexLLM` | Cortex API wrapper; live + mock modes; auto-logs every call | — |
| `PlanStore` | Execution plan CRUD | `inject_world_state_change()` |
| `ReflectionLogger` | Generate-critique round logging | — |
| `AgentMessageBus` | Inter-agent messaging | `create_deadlock()` |
| `MemoryStore` | AGENT_MEMORY CRUD | `poison_memory()` |
| `PatternEvaluator` | Decision-tree pattern recommender | — |

`CortexLLM` falls back to mock responses when live Cortex calls fail, so demos run offline.

## Notebook Structure (43 cells)

Cells are run top-to-bottom. Each pattern block follows the same structure:
1. Markdown introduction + figure cells
2. Working implementation
3. **Human Decision Node** (markdown + code cell pair)
4. Failure demonstration
5. Analysis

| Cells | Pattern | Failure Mode |
|-------|---------|-------------|
| 5–12 | ReAct (Reasoning + Acting) | Infinite loop (no `max_steps`, no done tool) → `LoopLimitError` |
| 13–19 | Plan-and-Execute | Stale plan after `inject_world_state_change()` |
| 20–24 | Reflection | Non-convergence / oscillation from contradictory criteria |
| 25–31 | Multi-Agent (Researcher → Writer → Reviewer) | Circular-wait deadlock via `create_deadlock()` |
| 32–36 | Memory-Augmented | Context poisoning via `poison_memory()` |
| 37–42 | Analytics & optional teardown | Cross-pattern Snowflake query analysis |

## Figures

`assets/diagrams/all_diagrams.md` contains Mermaid source for all 8 diagrams. PNGs are pre-generated in `assets/diagrams/`. Color convention: indigo = orchestrators, blue = stores, teal = executors, purple = planners, red = failures, amber = gates.

## Key Design Decisions

- **Framework-agnostic Python**: no LangGraph, AutoGen, etc. — explicit loops and gates are visible in code, not hidden behind abstractions.
- **Separate cells for working vs. failure**: failures are not flag-toggled variants; they are structurally different implementations.
- **All calls logged**: `LLM_CALL_LOG` records pattern name, call type (`working`/`failure`), latency, and token count for every Cortex invocation.
