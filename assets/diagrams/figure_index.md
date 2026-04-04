# Figure Index

> Complete registry of all Mermaid diagrams for Chapter 04.  
> Source file: [`all_diagrams.md`](all_diagrams.md)

| Figure # | Title | Pattern | Priority | Status | Placement in Chapter |
|----------|-------|---------|----------|--------|----------------------|
| 0 | Token Generation: Stateless Loop vs. Architectural Gate | Foundation — Token Generation | Critical | Complete | Section 4.1 — Before any pattern is introduced; establishes why architectural gates exist |
| 1 | ReAct: Think-Act-Observe Cycle with Dual Exit Paths | ReAct | Critical | Complete | Section 4.2 — ReAct pattern introduction; shows loop structure and failure mode |
| 2 | Plan-and-Execute: Stale Plan Failure Timeline | Plan-and-Execute | Critical | Complete | Section 4.3 — Plan-and-Execute failure analysis; timeline of stale assumption propagation |
| 2A | Plan-and-Execute: Normal State Architecture | Plan-and-Execute | Critical | Complete | Section 4.3 — Immediately after Figure 2; contrasts single-agent vs. separated architecture |
| 3 | Reflection: Convergence vs. Oscillation | Reflection | Critical | Complete | Section 4.4 — Reflection pattern; paired charts showing convergent vs. oscillating behavior |
| 3A | Criteria Quality vs. Model Quality: Ablation Grid | Reflection | Critical | Complete | Section 4.4 — After Figure 3; 2x2 grid proving criteria quality is the actionable variable |
| 4 | Multi-Agent Topology and Deadlock | Multi-Agent | Critical | Complete | Section 4.5 — Multi-agent introduction; topology diagram with deadlock overlay |
| 4A | Orchestrator Sequence Diagram | Multi-Agent | Critical | Complete | Section 4.5 — After Figure 4; swim-lane showing orchestrator routes but never executes |
| 5 | Memory-Augmented Architecture and Context Poisoning | Memory-Augmented | Important | Complete | Section 4.6 — Memory-augmented pattern; architecture with contamination path highlighted |
| 6 | Pattern Selection Decision Tree | All Patterns — Selection Guide | Important | Complete | Section 4.7 or Chapter Summary — Decision flowchart for choosing the right pattern |
| 7 | Capability vs. Architecture: Orthogonality Quadrant | All Patterns — Failure Taxonomy | Important | Complete | Section 4.7 or Chapter Summary — Final synthesis; maps all failure modes to one framework |

---

**Diagram types used:**

| Type | Count | Figures |
|------|-------|---------|
| Flowchart (`flowchart TB/LR`) | 7 | 0, 1, 2, 2A, 5, 6 |
| XY Chart (`xychart-beta`) | 2 | 3 (two charts) |
| Quadrant Chart (`quadrantChart`) | 2 | 3A, 7 |
| Sequence Diagram (`sequenceDiagram`) | 1 | 4A |

**Color palette:**

| Color | Hex | Usage |
|-------|-----|-------|
| Indigo | `#3730A3` | Orchestrators, root nodes, primary structural elements |
| Blue | `#2563EB` | Long-term stores, multi-agent pattern |
| Teal | `#0D9488` | Executors, specialists, ACT/OBSERVE nodes |
| Purple | `#7C3AED` | Planners, THINK nodes, agent cores, reflection |
| Green | `#16A34A` | Success states, exit conditions, validation |
| Amber | `#D97706` | Warnings, gates, force exits, plan-and-execute |
| Red | `#DC2626` | Failures, poisoned data, deadlocks, infinite loops |
| Slate | `#475569` | Model nodes, neutral structural elements |
| Gray | `#6B7280` | Buses, fallback nodes, secondary elements |
