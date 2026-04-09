# Five Patterns, Five Trade-offs

![Python 3.14](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![Snowflake Cortex](https://img.shields.io/badge/Snowflake-Cortex_LLM-29B5E8?logo=snowflake&logoColor=white)
![Status](https://img.shields.io/badge/Status-Complete-16A34A)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Chapter 4 of *Agentic Systems*: five agentic design patterns, each with a working implementation, a deliberate failure mode, and a mandatory human decision node -- all backed by Snowflake Cortex.**

> *Architecture is the leverage point, not the model. The pattern you choose determines what breaks -- not the model you use.*

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Jupyter Notebook                          │
│               chapter04_demo.ipynb                          │
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────┐  │
│  │  ReAct   │  │Plan-and- │  │Reflection│  │Multi-Agent│  │
│  │  Agent   │  │ Execute  │  │  Agent   │  │  System   │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └─────┬─────┘  │
│       │              │             │               │        │
│  ┌────┴──────────────┴─────────────┴───────────────┴────┐   │
│  │              snowflake/queries.py                     │   │
│  │   SnowflakeConnection · CortexLLM · MemoryStore      │   │
│  │   AgentMessageBus · ReflectionLogger · PlanStore      │   │
│  └──────────┬──────────────────────────┬────────────┘   │
│             │                          │                 │
└─────────────┼──────────────────────────┼─────────────────┘
              │                          │
    ┌─────────▼─────────┐    ┌──────────▼──────────┐
    │  Snowflake Cortex │    │   Snowflake DB      │
    │  (mistral-large)  │    │   AGENTIC_SYSTEMS_  │
    │                   │    │   BOOK.CHAPTER04    │
    │  LLM inference    │    │                     │
    │  via COMPLETE()   │    │  ┌───────────────┐  │
    └───────────────────┘    │  │ LLM_CALL_LOG  │  │
                             │  │ AGENT_MEMORY  │  │
                             │  │ AGENT_MESSAGES│  │
                             │  │ REFLECTION_   │  │
                             │  │   ROUNDS      │  │
                             │  │ EXECUTION_    │  │
                             │  │   PLANS       │  │
                             │  │ PATTERN_      │  │
                             │  │  EVALUATIONS  │  │
                             │  └───────────────┘  │
                             └─────────────────────┘
```

Every LLM call is logged with latency and token count. Every failure is recorded with a timestamp. Every memory operation -- including the poisoned one -- persists in a table you can query.

---

## Prerequisites

- **Snowflake account** with [Cortex LLM functions](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions) enabled
- **Python 3.10+** (developed on 3.14)
- **Jupyter Notebook** or JupyterLab

---

## Setup

```bash
# 1. Clone the repository
git clone https://github.com/raghuneu/Five-Patterns.git && cd Five-Patterns

# 2. Create environment file
cp .env.example .env

# 3. Fill in your Snowflake credentials in .env
#    SNOWFLAKE_ACCOUNT=<your-account>
#    SNOWFLAKE_USER=<your-user>
#    SNOWFLAKE_PASSWORD=<your-password>
#    SNOWFLAKE_WAREHOUSE=AGENTIC_DEMO_WH
#    SNOWFLAKE_DATABASE=AGENTIC_SYSTEMS_BOOK
#    SNOWFLAKE_SCHEMA=CHAPTER04
#    CORTEX_MODEL=mistral-large

# 4. Run the setup script in a Snowflake worksheet
#    Open snowflake/setup.sql and execute it.
#    This creates the database, schema, warehouse, and all 6 tables.

# 5. Launch the notebook
pip install snowflake-connector-python python-dotenv pandas matplotlib
jupyter notebook notebook/chapter04_demo.ipynb
```

---

## Notebook Contents

The notebook has 30 cells organized into five pattern sections plus setup and analytics.

| Cell | Type | Content |
|------|------|---------|
| 0 | Markdown | Title, core claim, notebook overview |
| 1 | Code | `pip install` dependencies |
| 2 | Code | Imports and infrastructure initialization |
| 3 | Code | Run `setup.sql` and verify Cortex connection |
| **4** | **Markdown** | **Pattern 1: ReAct** -- introduction and failure mode description |
| 5 | Code | Tool registry: `search`, `calculator`, `summarize`, `done` |
| 6 | Code | Working ReAct agent (`max_steps=5`, `done` tool enabled) |
| **7** | **Markdown** | **Human Decision Node -- Pattern 1** |
| 8 | Code | FAILURE: ReAct infinite loop (no `done` tool, no `max_steps`) |
| 9 | Code | LLM call log analysis for ReAct |
| **10** | **Markdown** | **Pattern 2: Plan-and-Execute** -- introduction and failure mode description |
| 11 | Code | Working Plan-and-Execute agent (4-step plan with world state) |
| **12** | **Markdown** | **Human Decision Node -- Pattern 2** |
| 13 | Code | FAILURE: Stale plan (world state change injected at step 3) |
| **14** | **Markdown** | **Pattern 3: Reflection** -- introduction and failure mode description |
| 15 | Code | Working Reflection agent (coherent criteria, `threshold=7.5`) |
| **16** | **Markdown** | **Human Decision Node -- Pattern 3** |
| 17 | Code | FAILURE: Non-converging reflection (contradictory criteria) + plot |
| **18** | **Markdown** | **Pattern 4: Multi-Agent** -- introduction and failure mode description |
| 19 | Code | Working Multi-Agent system (Researcher -> Writer -> Reviewer) |
| **20** | **Markdown** | **Human Decision Node -- Pattern 4** |
| 21 | Code | FAILURE: Circular-wait deadlock between Writer and Reviewer |
| **22** | **Markdown** | **Pattern 5: Memory-Augmented** -- introduction and failure mode description |
| 23 | Code | Working Memory-Augmented agent (keyword retrieval from `AGENT_MEMORY`) |
| **24** | **Markdown** | **Human Decision Node -- Pattern 5** |
| 25 | Code | FAILURE: Context poisoning (corrupted memory retrieved as ground truth) |
| 26 | Code | Pattern Recommender -- cross-pattern evaluation |
| 27 | Code | Full demo analytics from Snowflake (call log, evaluations) |
| **28** | **Markdown** | **Closing** -- summary and architectural lessons |
| 29 | Code | Cleanup (optional teardown) |

---

## Failure Triggers

Each pattern has a dedicated failure cell. The failure is architectural, not parametric.

| Pattern | Cell | Trigger | Expected Output |
|---------|------|---------|-----------------|
| **ReAct** | 8 | `done` tool removed from registry; no `max_steps` guard | Agent loops 8 iterations (safety limit), never converges. Raises `LoopLimitError`. |
| **Plan-and-Execute** | 13 | `inject_world_state_change(3)` called between steps 2 and 3 | Steps 3-4 execute against stale schema (v2 vs. v3). Output is structurally valid, semantically wrong. No exception raised. |
| **Reflection** | 17 | `criteria=["extreme_conciseness", "comprehensive_detail"]`, `threshold=9.0` | Score oscillates between rounds, never crosses threshold. Matplotlib plot shows non-convergence. |
| **Multi-Agent** | 21 | `bus.create_deadlock("writer", "reviewer")` marks pending messages as `'deadlocked'` | Both agents timeout waiting for each other. Raises `DeadlockError`. |
| **Memory-Augmented** | 25 | `mem.poison_memory(memory_id, false_content)` overwrites a valid memory with `is_poisoned=TRUE` | Agent retrieves poisoned record identically to valid ones. Produces fluent, confident, wrong answer. |

---

## The Human Decision Node

Each pattern section includes a mandatory human decision node (cells 7, 12, 16, 20, 24). The format is identical across all five:

> **BEFORE PROCEEDING -- Verify for your use case:**
> - [ ] *[Pattern-specific architectural assumption 1]*
> - [ ] *[Pattern-specific architectural assumption 2]*
> - [ ] *[Pattern-specific architectural assumption 3]*
>
> **HUMAN DECISION:** [Document your verification here]
> **ARCHITECTURAL REASONING:** [Document here]

The human decision node is not a suggestion. It is an architectural checkpoint that forces the reader to verify the pattern's assumptions against their specific use case before running the failure demonstration. The working implementation and the failure case are in separate cells -- not toggled by a flag -- because a flag-toggled failure can be dismissed as artificial. A separate cell with a separately documented decision node makes the failure mode a first-class architectural demonstration.

---

## Project Structure

```
Five-Patterns/
├── README.md                           # This file
├── .env.example                        # Snowflake credentials template
├── LICENSE                             # MIT
├── snowflake/
│   ├── setup.sql                       # Database + 6 tables provisioning
│   ├── teardown.sql                    # Cleanup script
│   └── queries.py                      # 7 classes: connection, LLM, stores, bus, logger
├── chapter/
│   ├── chapter04.md                    # Main chapter prose
│   ├── chapter04.html                  # Substack-ready HTML
│   └── authors_note.md                 # 3-page Author's Note
├── notebook/
│   └── chapter04_demo.ipynb            # Main Jupyter demo (30 cells)
├── figures/
│   └── figure_prompts.md               # Figure Architect prompts
├── assets/
│   └── diagrams/
│       ├── all_diagrams.md             # 12 Mermaid diagrams
│       └── figure_index.md             # Figure registry and metadata
└── submission/
    └── checklist.md                    # Pre-submission checklist
```

---

## Figures

| Figure | File | Section |
|--------|------|---------|
| Hero | assets/hero/hero.png | Cover |
| Fig 0 | assets/diagrams/Fig 0.png | Introduction |
| Fig 1 | assets/diagrams/Fig 1.png | Pattern 1: ReAct |
| Fig 2 | assets/diagrams/Fig 2.png | Pattern 2: Failure |
| Fig 2A | assets/diagrams/Fig 2A.png | Pattern 2: Mechanism |
| Fig 3 Convergence | assets/diagrams/Fig 3 Convergence.png | Pattern 3: Working |
| Fig 3 Oscillation | assets/diagrams/Fig 3 Oscillation.png | Pattern 3: Failure |
| Fig 3A | assets/diagrams/Fig 3A.png | Pattern 3: Mechanism |
| Fig 4 | assets/diagrams/Fig 4.png | Pattern 4: Failure |
| Fig 4A | assets/diagrams/Fig 4A.png | Pattern 4: Mechanism |
| Fig 5 | assets/diagrams/Fig 5.png | Pattern 5: Memory |
| Fig 6 | assets/diagrams/Fig 6.png | Pattern Selection |
| Fig 7 | assets/diagrams/Fig 7.png | Closing |

---

## Video Walkthrough

**Show-and-Tell (10 min) — Explain → Show → Try**

> Link: <!-- TODO: paste YouTube/Vimeo URL here -->

Covers all five patterns, five failure demonstrations, and the Multi-Agent Human Decision Node (S13) where the AI's "prompt confusion" framing was rejected in favor of the architectural deadlock diagnosis.

---

## Teardown

To drop all objects and reset for a clean run:

```sql
-- Execute snowflake/teardown.sql in a Snowflake worksheet
```

---

## License

[MIT](LICENSE) -- Copyright (c) 2026 Raghu Ram
