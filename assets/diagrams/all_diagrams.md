# All Mermaid Diagrams

> **Color Palette Reference**
> Indigo `#3730A3` · Blue `#2563EB` · Teal `#0D9488` · Green `#16A34A` · Amber `#D97706` · Red `#DC2626` · Slate `#475569` · Light Gray `#F3F4F6`

---

## Figure 0 — Token Generation: Stateless Loop vs. Architectural Gate

**Pattern:** Foundation — Token Generation  
**Priority:** Critical

```mermaid
flowchart LR
    subgraph LEFT ["<b>No architectural gate</b>"]
        direction TB
        A1["📥 Input Sequence"]:::slateblue
        A2["🧠 Language Model<br/><i>next-token predictor</i>"]:::slateblue
        A3["🎲 Sampled Token"]:::slateblue
        A1 --> A2 --> A3
        A3 -- "append to sequence" --> A1
    end

    subgraph RIGHT ["<b>With architectural gate</b>"]
        direction TB
        B1["📥 Input Sequence"]:::slateblue
        B2["🧠 Language Model<br/><i>next-token predictor</i>"]:::slateblue
        B3["🎲 Sampled Token"]:::slateblue
        B4{"🚧 External Gate<br/><code>done_signal?</code><br/><code>max_steps?</code>"}:::amber
        B5["✅ Return Answer"]:::green

        B1 --> B2 --> B3
        B3 --> B4
        B4 -- "NO — continue" --> B1
        B4 -- "YES — exit" --> B5
    end

    LEFT ~~~ RIGHT

    style LEFT fill:#FEF2F2,stroke:#DC2626,stroke-width:2px,color:#1E1B4B
    style RIGHT fill:#F0FDF4,stroke:#16A34A,stroke-width:2px,color:#1E1B4B

    classDef slateblue fill:#475569,stroke:#1E293B,color:#F8FAFC,stroke-width:2px
    classDef amber fill:#D97706,stroke:#92400E,color:#FFFBEB,stroke-width:2px
    classDef green fill:#16A34A,stroke:#166534,color:#F0FDF4,stroke-width:2px
    classDef red fill:#DC2626,stroke:#991B1B,color:#FEF2F2,stroke-width:2px

    linkStyle 2 stroke:#DC2626,stroke-width:3px
```

> **Left panel:** The token loop has no intrinsic exit — it runs until an external timeout or cost limit intervenes.  
> **Right panel:** An **External Gate** sits outside the model, evaluating `done_signal` or `max_steps`. Termination is an architectural property, not a model property.

*Figure 0. Token generation has no intrinsic termination condition (left). The loop limit and done signal are architectural gates that sit outside the model (right).*

---

## Figure 1 — ReAct: Think-Act-Observe Cycle with Dual Exit Paths

**Pattern:** ReAct  
**Priority:** Critical

```mermaid
flowchart TB
    subgraph REACT_LOOP ["ReAct loop <i>(bounded by max_steps)</i>"]
        direction TB
        THINK["💭 <b>THINK</b><br/>Reasoning trace generation"]:::purple
        ACT["⚡ <b>ACT</b><br/>Tool call execution"]:::teal
        OBSERVE["👁️ <b>OBSERVE</b><br/>Environment response"]:::teal

        THINK --> ACT
        ACT --> OBSERVE
        OBSERVE -- "feedback" --> THINK
    end

    DONE["✅ <b>Done</b><br/>Return Answer"]:::green
    FORCE["⚠️ <b>Force Exit</b><br/>Best Answer So Far"]:::amber
    FAIL["💀 <b>FAILURE</b><br/>Infinite reasoning loop"]:::red

    THINK -- "FINISH signal<br/>detected" --> DONE
    THINK -- "max_steps<br/>reached" --> FORCE
    THINK -. "NO exit conditions →<br/>loops indefinitely" .-> FAIL

    style REACT_LOOP fill:#F5F3FF,stroke:#6D28D9,stroke-width:2px,stroke-dasharray:8 4,color:#1E1B4B

    classDef purple fill:#7C3AED,stroke:#4C1D95,color:#F5F3FF,stroke-width:2px
    classDef teal fill:#0D9488,stroke:#115E59,color:#F0FDFA,stroke-width:2px
    classDef green fill:#16A34A,stroke:#166534,color:#F0FDF4,stroke-width:2px
    classDef amber fill:#D97706,stroke:#92400E,color:#FFFBEB,stroke-width:2px
    classDef red fill:#DC2626,stroke:#991B1B,color:#FEF2F2,stroke-width:2px

    linkStyle 5 stroke:#DC2626,stroke-width:2px,stroke-dasharray:6 3
```

*Figure 1. Two exit conditions bound the ReAct loop. Removing either — especially max_steps — eliminates the architecture's only termination constraint.*

---

## Figure 2 — Plan-and-Execute: Stale Plan Failure Timeline

**Pattern:** Plan-and-Execute  
**Priority:** Critical

```mermaid
flowchart LR
    T0["<b>T=0</b><br/>🗓️ <b>Planner</b><br/>Creates plan<br/>Assumption: <code>Schema v1</code>"]:::purple
    T1["<b>T=1</b><br/>⚙️ <b>Executor</b><br/>Step 1 ✅<br/><i>Succeeds</i>"]:::green
    T2["<b>T=2</b><br/>💥 <b>World Change</b><br/><code>Schema → v2</code>"]:::red
    T3["<b>T=3</b><br/>⚙️ <b>Executor</b><br/>Still using<br/><code>Schema v1</code>"]:::teal
    OUT["⚠️ <b>Output</b><br/>Structurally valid<br/>Semantically wrong<br/><i>No exception raised</i>"]:::amber

    T0 --> T1 --> T2 --> T3 --> OUT
    T0 -. "stale assumption<br/>propagates silently" .-> T3

    classDef purple fill:#7C3AED,stroke:#4C1D95,color:#F5F3FF,stroke-width:2px
    classDef teal fill:#0D9488,stroke:#115E59,color:#F0FDFA,stroke-width:2px
    classDef green fill:#16A34A,stroke:#166534,color:#F0FDF4,stroke-width:2px
    classDef amber fill:#D97706,stroke:#92400E,color:#FFFBEB,stroke-width:2px
    classDef red fill:#DC2626,stroke:#991B1B,color:#FEF2F2,stroke-width:2px

    linkStyle 4 stroke:#DC2626,stroke-width:2px,stroke-dasharray:6 3
```

*Figure 2. The planner commits to Schema v1 at T=0. When the world changes at T=2, the executor has no mechanism to detect the divergence. The output looks correct. It is wrong.*

---

## Figure 2A — Plan-and-Execute: Normal State Architecture

**Pattern:** Plan-and-Execute  
**Priority:** Critical

```mermaid
flowchart TB
    subgraph LEFT ["<b>Single agent — full context</b>"]
        direction TB
        SA_IN["🎯 Full Goal"]:::slateblue
        SA_AGENT["🧠 Single Agent<br/><i>makes all tool calls,<br/>generates output</i>"]:::slateblue
        SA_CTX["📚 Context accumulates<br/>over time"]:::lightgray
        SA_OUT["📤 Output"]:::slateblue

        SA_IN --> SA_AGENT
        SA_AGENT <--> |"context"| SA_CTX
        SA_AGENT --> SA_OUT
    end

    subgraph RIGHT ["<b>Separated architecture</b>"]
        direction TB
        R_GOAL["🎯 Full Goal"]:::purple
        R_PLAN["📋 <b>PLANNER</b><br/>Receives full goal<br/>Outputs complete task list"]:::purple
        R_BOUNDARY["━━━━ CONTEXT BOUNDARY ━━━━<br/><i>Executor sees ONE task.<br/>Full goal is invisible.</i>"]:::boundary
        R_EXEC["⚙️ <b>EXECUTOR</b><br/>Receives single task only<br/><i>No access to full goal<br/>or remaining plan</i>"]:::teal
        R_FEEDBACK["↩️ Step output feeds<br/>back to Planner only"]:::lightgray

        R_GOAL --> R_PLAN
        R_PLAN --> R_BOUNDARY
        R_BOUNDARY --> R_EXEC
        R_EXEC --> R_FEEDBACK
        R_FEEDBACK --> R_PLAN
    end

    LEFT ~~~ RIGHT

    style LEFT fill:#F8FAFC,stroke:#475569,stroke-width:2px,color:#1E1B4B
    style RIGHT fill:#F5F3FF,stroke:#6D28D9,stroke-width:2px,color:#1E1B4B

    classDef slateblue fill:#475569,stroke:#1E293B,color:#F8FAFC,stroke-width:2px
    classDef purple fill:#7C3AED,stroke:#4C1D95,color:#F5F3FF,stroke-width:2px
    classDef teal fill:#0D9488,stroke:#115E59,color:#F0FDFA,stroke-width:2px
    classDef boundary fill:#FEF3C7,stroke:#D97706,stroke-width:3px,color:#92400E
    classDef lightgray fill:#F3F4F6,stroke:#9CA3AF,color:#374151,stroke-width:1px
```

*Figure 2A. Separation means each component sees only what it needs. This prevents goal drift but creates the stale plan vulnerability — the executor cannot detect when its task assumptions are invalidated.*

---

## Figure 3 — Reflection: Convergence vs. Oscillation

**Pattern:** Reflection  
**Priority:** Critical

```mermaid
---
config:
  theme: base
  themeVariables:
    primaryColor: "#3730A3"
    lineColor: "#475569"
---
xychart-beta
    title "Coherent criteria — convergence"
    x-axis "Round" [1, 2, 3, 4, 5, 6, 7, 8]
    y-axis "Critic Score" 0.0 --> 1.0
    line "Score" [0.52, 0.61, 0.70, 0.78, 0.85, 0.88, 0.90, 0.91]
    line "Threshold (0.85)" [0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85]
```

```mermaid
---
config:
  theme: base
  themeVariables:
    primaryColor: "#DC2626"
    lineColor: "#DC2626"
---
xychart-beta
    title "Contradictory criteria — oscillation"
    x-axis "Round" [1, 2, 3, 4, 5, 6, 7, 8]
    y-axis "Critic Score" 0.0 --> 1.0
    line "Score" [0.60, 0.78, 0.62, 0.76, 0.64, 0.79, 0.61, 0.77]
    line "Threshold (0.85)" [0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85]
```

> **Left chart (Coherent criteria):** Blue score line rises monotonically from ~0.52 to ~0.91, crossing the 0.85 threshold at round 5. ✅ **Converged.**  
> **Right chart (Contradictory criteria):** Red score line alternates between ~0.60 and ~0.80 for all 8 rounds, never crossing threshold. ❌ **Never converges.**

*Figure 3. Oscillating scores are the diagnostic signature of contradictory criteria. The fix is always criteria revision — never model upgrade.*

---

## Figure 3A — Criteria Quality vs. Model Quality: Ablation Grid

**Pattern:** Reflection  
**Priority:** Critical

```mermaid
---
config:
  quadrantChart:
    chartWidth: 600
    chartHeight: 600
    quadrantLabelFontSize: 14
    pointLabelFontSize: 0
---
quadrantChart
    title Criteria Quality vs. Model Quality
    x-axis "Weak Model" --> "Strong Model"
    y-axis "Contradictory Criteria" --> "Clear Criteria"
    quadrant-1 "Converges faster (ideal)"
    quadrant-2 "Converges (criteria compensate)"
    quadrant-3 "Oscillates (both misaligned)"
    quadrant-4 "Oscillates fluently (DANGER)"
```

> | | **Weak Model** | **Strong Model** |
> |---|---|---|
> | **Clear Criteria** | ✅ Converges — criteria coherence compensates for model weakness | ✅ Converges faster — both factors aligned (ideal) |
> | **Contradictory Criteria** | ❌ Oscillates — both factors misaligned | ⚠️ **Oscillates fluently** — DANGER: failure is harder to detect |

*Figure 3A. Criteria quality is the actionable determinant. A stronger model with contradictory criteria oscillates more articulately — making the failure harder to detect, not easier to fix.*

---

## Figure 4 — Multi-Agent Topology and Deadlock

**Pattern:** Multi-Agent  
**Priority:** Critical

```mermaid
flowchart TB
    ORCH["🎛️ <b>ORCHESTRATOR</b>"]:::indigo

    subgraph BUS ["Shared Message Bus"]
        direction LR
        BUS_L[" "]:::bus
        BUS_R[" "]:::bus
    end

    RES["🔬 <b>Researcher</b>"]:::teal

    subgraph DEADLOCK ["⚠️ Circular wait — DEADLOCK"]
        direction LR
        WRI["✍️ <b>Writer</b>"]:::teal
        REV["🔍 <b>Reviewer</b>"]:::teal
    end

    ORCH <--> |"route / collect"| BUS
    BUS <--> |"normal flow"| RES
    BUS <--> |"normal flow"| WRI
    BUS <--> |"normal flow"| REV

    WRI -. "⏳ awaiting response<br/>from Reviewer" .-> REV
    REV -. "⏳ awaiting response<br/>from Writer" .-> WRI

    style BUS fill:#E5E7EB,stroke:#6B7280,stroke-width:2px,color:#374151
    style DEADLOCK fill:#FEF2F2,stroke:#DC2626,stroke-width:3px,stroke-dasharray:8 4,color:#991B1B

    classDef indigo fill:#3730A3,stroke:#1E1B4B,color:#EEF2FF,stroke-width:3px
    classDef teal fill:#0D9488,stroke:#115E59,color:#F0FDFA,stroke-width:2px
    classDef bus fill:#E5E7EB,stroke:#9CA3AF,color:#E5E7EB,stroke-width:0px

    linkStyle 4 stroke:#DC2626,stroke-width:2px,stroke-dasharray:6 3
    linkStyle 5 stroke:#DC2626,stroke-width:2px,stroke-dasharray:6 3
```

> **Legend:**
> - 🟦 Indigo = Orchestrator
> - 🟩 Teal = Specialist agents
> - ➡️ Blue arrows = Normal message flow
> - 🔴 Red dashed arrows = Deadlock circular-wait

*Figure 4. Deadlock is topological — it emerges from the handoff protocol, not from any individual agent's failure. Both agents are functioning correctly. Neither will proceed.*

---

## Figure 4A — Orchestrator Sequence Diagram

**Pattern:** Multi-Agent  
**Priority:** Critical

```mermaid
sequenceDiagram
    box rgb(238,242,255) External
        participant EXT as 📨 External Request
    end
    box rgb(224,231,255) Orchestrator
        participant ORCH as 🎛️ Orchestrator
    end
    box rgb(240,253,250) Specialists
        participant RES as 🔬 Researcher
        participant WRI as ✍️ Writer
    end

    EXT->>ORCH: "Research and write report on X"
    activate ORCH

    Note over ORCH: ROUTE task to Researcher
    ORCH->>RES: Assign research task
    activate RES

    Note over RES: 🔧 EXECUTE tool calls<br/>(tool calls happen HERE)
    RES-->>ORCH: Return research notes
    deactivate RES

    Note over ORCH: ROUTE notes to Writer
    ORCH->>WRI: Assign writing task + notes
    activate WRI

    Note over WRI: 🔧 EXECUTE tool calls<br/>(tool calls happen HERE)
    WRI-->>ORCH: Return draft
    deactivate WRI

    Note over ORCH: 📦 Assemble outputs
    ORCH-->>EXT: Final output
    deactivate ORCH

    Note right of ORCH: ⛔ DOES NOT EXECUTE —<br/>tool calls never enter<br/>Orchestrator lane
```

*Figure 4A. The Orchestrator routes and assembles. It never calls a tool directly. Execution is always inside the specialist's swim lane.*

---

## Figure 5 — Memory-Augmented Architecture and Context Poisoning

**Pattern:** Memory-Augmented  
**Priority:** Important

```mermaid
flowchart TB
    STM["💬 <b>Short-term Memory</b><br/><i>Current session —<br/>context window</i>"]:::lightblue
    AGENT["🧠 <b>Agent</b>"]:::purple
    RETRIEVAL["🔎 <b>Retrieval Layer</b>"]:::gray
    LTM["🗄️ <b>Long-term Store</b><br/><i>AGENT_MEMORY —<br/>external store</i>"]:::blue
    POISON["☠️ <b>Poisoned Record</b><br/><code>is_poisoned=TRUE</code>"]:::red
    VALID["🛡️ <b>Validation Check</b><br/><i>Absent defense ⚠️</i>"]:::green
    OUTPUT["📤 <b>Output</b>"]:::amber

    AGENT <--> |"bidirectional"| STM
    AGENT -- "write path" --> VALID
    VALID -- "store" --> LTM
    LTM -- "retrieve" --> RETRIEVAL
    RETRIEVAL -- "inject into<br/>context" --> AGENT
    AGENT --> OUTPUT

    POISON -- "retrieved as<br/>ground truth" --> RETRIEVAL
    POISON -.-> LTM

    OUTPUT_BAD["🔴 <b>Fluent, confident,<br/>wrong answer</b>"]:::red
    POISON -. "contaminates" .-> OUTPUT_BAD

    style VALID stroke-dasharray:5 5

    classDef purple fill:#7C3AED,stroke:#4C1D95,color:#F5F3FF,stroke-width:2px
    classDef blue fill:#2563EB,stroke:#1E40AF,color:#EFF6FF,stroke-width:2px
    classDef lightblue fill:#BFDBFE,stroke:#3B82F6,color:#1E3A5F,stroke-width:2px
    classDef teal fill:#0D9488,stroke:#115E59,color:#F0FDFA,stroke-width:2px
    classDef green fill:#16A34A,stroke:#166534,color:#F0FDF4,stroke-width:2px,stroke-dasharray:5 5
    classDef amber fill:#D97706,stroke:#92400E,color:#FFFBEB,stroke-width:2px
    classDef red fill:#DC2626,stroke:#991B1B,color:#FEF2F2,stroke-width:2px
    classDef gray fill:#9CA3AF,stroke:#6B7280,color:#F9FAFB,stroke-width:2px

    linkStyle 6 stroke:#DC2626,stroke-width:2px,stroke-dasharray:6 3
    linkStyle 7 stroke:#DC2626,stroke-width:1px,stroke-dasharray:4 2
    linkStyle 8 stroke:#DC2626,stroke-width:2px,stroke-dasharray:6 3
```

> **Poisoning path:** A poisoned record in the long-term store is indistinguishable from a valid record at retrieval time. The Validation Check sits on the **write** path — it cannot intercept a record already in the store.

*Figure 5. The retrieval layer trusts all stored memories equally. A poisoned record is indistinguishable from a valid one. The validation gate sits on the write path — it cannot intercept a record already in the store.*

---

## Figure 6 — Pattern Selection Decision Tree

**Pattern:** All Patterns — Selection Guide  
**Priority:** Important

```mermaid
flowchart TB
    START(["🆕 <b>New Task</b>"]):::indigo

    Q1{"Stable, ordered<br/>subtasks?"}:::diamond
    Q2{"Dynamic tool use<br/>with observable results?"}:::diamond
    Q3{"Output quality verifiable<br/>against criteria?"}:::diamond
    Q4{"Task spans multiple<br/>specialist domains?"}:::diamond
    Q5{"Requires context from<br/>previous sessions?"}:::diamond

    PE["📋 <b>Plan-and-Execute</b><br/><i>Planner creates full task list;<br/>Executor runs tasks one at a time</i>"]:::amber
    RA["🔄 <b>ReAct</b><br/><i>Think → Act → Observe loop<br/>with bounded steps</i>"]:::teal
    RF["🔍 <b>Reflection</b><br/><i>Generate → Critique → Revise<br/>with coherent quality threshold</i>"]:::purple
    MA["🤝 <b>Multi-Agent</b><br/><i>Orchestrator routes; specialists<br/>execute via message bus</i>"]:::blue
    MEM["🧠 <b>Memory-Augmented</b><br/><i>Retrieves from persistent store;<br/>incorporates into context</i>"]:::green

    SIMPLE["💡 <b>Start with simplest pattern</b><br/><i>Complexity is a cost,<br/>not a feature</i>"]:::gray

    START --> Q1
    Q1 -- "YES" --> PE
    Q1 -- "NO" --> Q2
    Q2 -- "YES" --> RA
    Q2 -- "NO" --> Q3
    Q3 -- "YES" --> RF
    Q3 -- "NO" --> Q4
    Q4 -- "YES" --> MA
    Q4 -- "NO" --> Q5
    Q5 -- "YES" --> MEM
    Q5 -- "NO" --> SIMPLE

    classDef indigo fill:#3730A3,stroke:#1E1B4B,color:#EEF2FF,stroke-width:3px
    classDef diamond fill:#F3F4F6,stroke:#475569,color:#1E1B4B,stroke-width:2px
    classDef amber fill:#D97706,stroke:#92400E,color:#FFFBEB,stroke-width:2px
    classDef teal fill:#0D9488,stroke:#115E59,color:#F0FDFA,stroke-width:2px
    classDef purple fill:#7C3AED,stroke:#4C1D95,color:#F5F3FF,stroke-width:2px
    classDef blue fill:#2563EB,stroke:#1E40AF,color:#EFF6FF,stroke-width:2px
    classDef green fill:#16A34A,stroke:#166534,color:#F0FDF4,stroke-width:2px
    classDef gray fill:#6B7280,stroke:#374151,color:#F9FAFB,stroke-width:2px,stroke-dasharray:4 2

    linkStyle 1 stroke:#16A34A,stroke-width:2px
    linkStyle 3 stroke:#16A34A,stroke-width:2px
    linkStyle 5 stroke:#16A34A,stroke-width:2px
    linkStyle 7 stroke:#16A34A,stroke-width:2px
    linkStyle 9 stroke:#16A34A,stroke-width:2px
```

*Figure 6. Work through these questions in order. The first YES determines your pattern. If no YES is reached, the simplest pattern is the right choice.*

---

## Figure 7 — Capability vs. Architecture: Orthogonality Quadrant

**Pattern:** All Patterns — Failure Taxonomy  
**Priority:** Important

```mermaid
---
config:
  quadrantChart:
    chartWidth: 600
    chartHeight: 600
    quadrantLabelFontSize: 14
    pointLabelFontSize: 12
    pointRadius: 6
---
quadrantChart
    title Capability vs. Architecture
    x-axis "Low Capability" --> "High Capability"
    y-axis "Low Arch. Soundness" --> "High Arch. Soundness"
    quadrant-1 "RELIABLE (target state)"
    quadrant-2 "Constrained and safe"
    quadrant-3 "Breaks quietly"
    quadrant-4 "BREAKS CONVINCINGLY"
    "ReAct no loop limit": [0.75, 0.20]
    "Reflection bad criteria": [0.80, 0.25]
    "Memory no validation": [0.70, 0.15]
```

> **Bottom-right quadrant (DANGER ZONE)** contains all three example failure points:
> - ReAct without loop limit
> - Reflection with contradictory criteria
> - Memory without validation layer
>
> **Key insight:** Higher capability → more articulate failure → harder to detect.

*Figure 7. Model capability and architectural soundness operate on independent axes. Improving the model does not close an architectural gap — it makes the gap harder to see. The failure modes in this chapter all live in the bottom-right quadrant.*

---

> **End of diagrams.** See `figure_index.md` for the complete figure registry.
