# Figure Architect Analysis

## Chapter 4: Five Patterns, Five Trade-offs

### _Design of Agentic Systems with Case Studies_

---

## Phase 0: Hero Image Prompt

**HERO IMAGE — Architectural Constraints as Control in Agentic Systems**

### Structural Prompt

_(for BioRender / Illustrae / AI diagram tools)_

> "Generate a full-bleed, text-free hero image representing the idea that structure — not intelligence — determines reliability in autonomous systems. Show five distinct geometric forms, each suggesting a different kind of boundary or containment, arranged in a radial composition around a central form that pulses with implied energy. Each outer form constrains or channels the central energy in a different way: a loop with a wall, a branching path with sealed endpoints, a recursive mirror with a floor, a mesh of nodes with defined corridors, and a layered store with a locked gate. Use a centered composition with radial symmetry. No labels, legends, annotations, text, numbers, or symbols of any kind. Style: clean scientific illustration, white background, slate blue and soft amber palette with cool gray structural elements."

### Aesthetic Prompt

_(for Midjourney v6.1)_

> "Five geometric containment forms arranged radially around a glowing central node, each form channeling light differently — a sealed loop, a branching channel, a reflective floor, a mesh corridor, a layered vault, matte finish, slate blue and warm amber on cool gray, diffuse overcast lighting, centered radial composition, no text, no labels, no numbers, no annotations, graphical abstract, publication hero image, peer-review quality --v 6.1 --style raw --stylize 75 --no text, letters, words, numbers, labels, annotations, watermarks, cinematic, glow, neon, bokeh, plastic, 3D render artifacts, watercolor, collage"

### Hero Checklist

- [ ] Zero text, labels, or numbers present anywhere in the image
- [ ] Conveys "constraint as the unit of control" without literal depiction
- [ ] Slate blue / amber / gray palette is colorblind-accessible
- [ ] Radial composition works at full-bleed and thumbnail scale
- [ ] No decorative elements distract from the central visual metaphor
- [ ] Suitable for journal cover, article header, and social media card simultaneously

> **Note:** The Hero Image is always ranked separately and is considered **mandatory infrastructure** — it is not ranked against analytical figures.

---

## Summary

This is a mechanistic/technical chapter covering five distinct agentic architectural patterns, each with an embedded causal failure theory. The visual gaps are substantial: every failure mode is described as a causal chain that is nearly impossible to verify from prose alone, and the trade-off comparison table makes quantitative claims (latency, reliability, complexity) that demand graphical treatment. The highest-risk zones for the Eddy the Editor audit are the sections where failure modes are described verbally but no mechanism diagram shows _why_ the architecture permits the failure — readers are asked to trust the author's causal logic without any structural anchor.

---

## Phase 1 & 2: High-Assertion Zone Detection + Figure Recommendation Table

| #   | Text Location (first 8 words)                                                           | Heuristic | Recommended Figure Type                                                       | Rationale                                                                                                                |
| --- | --------------------------------------------------------------------------------------- | --------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| 1   | "The ReAct pattern operates through a three-step cycle"                                 | MC        | Cycle diagram (looped flowchart with exit paths)                              | Three interdependent steps with two distinct exit conditions; reader cannot visualize loop topology from prose           |
| 2   | "the loop limit is not optional. It is the architectural constraint"                    | VG        | Annotated comparison diagram (with vs. without loop limit)                    | Core architectural claim — loop limit as safety vs. done signal as utility — is asserted without spatial proof           |
| 3   | "Infinite reasoning loop. The causal chain: the loop limit is removed"                  | MC + VG   | Causal chain / failure path diagram                                           | The failure mechanism is a 5-step causal sequence; readers cannot trace it without a visual path                         |
| 4   | "Plan-and-Execute separates the reasoning about what to do"                             | MC        | Two-phase architectural diagram (Planner → Executor with dependency arrows)   | Planner/Executor separation with sequential dependency is the core structural claim; not verifiable from text            |
| 5   | "Stale plan execution. The causal chain: the planner creates a plan"                    | MC + VG   | Causal chain / timeline divergence diagram                                    | T=0 plan vs. T=2 world-state divergence is a temporal architecture claim that requires a timeline to be credible         |
| 6   | "The Reflection pattern separates a generative pass from an evaluative pass"            | MC        | Generator-Critic loop diagram with score threshold                            | Three-component feedback loop (generate → critique → revise) with two exit conditions; structurally non-obvious          |
| 7   | "Non-converging reflection. The causal chain: the criteria set includes two standards"  | PQ        | Convergence / oscillation graph (score vs. round)                             | The oscillation signature is quantitative; prose says scores "alternate between two values" — this demands a chart       |
| 8   | "The multi-agent pattern distributes a complex task across multiple specialized agents" | MC + VG   | Topology diagram (message bus with agent roles and handoff protocols)         | Four-agent coordination with a shared message bus is a spatial architecture claim; cannot be understood from prose alone |
| 9   | "Coordination deadlock. The causal chain: Agent A is configured to await"               | VG        | Circular dependency diagram (deadlock state with pending arrows)              | Deadlock is a _topological_ failure — circular waiting — that is definitionally a visual concept                         |
| 10  | "Memory-augmented agents maintain two distinct memory stores"                           | MC + VG   | Dual-store architecture diagram (short-term / long-term with retrieval layer) | Two stores + retrieval layer + write path is a 4-component architecture; prose describes it but cannot ground it         |
| 11  | "Context poisoning. The causal chain: a false memory is written"                        | MC + VG   | Causal chain / contamination flow diagram                                     | A 4-step silent failure path (write → retrieve → incorporate → output) requires visual tracing to be credible            |
| 12  | "When you face a new task, work through these diagnostic questions"                     | MC        | Decision tree / pattern selection flowchart                                   | 5-question diagnostic with branching logic is a decision tree by definition; prose form buries the branching logic       |
| 13  | "Read this table as a constraint map, not a leaderboard"                                | PQ        | Annotated radar/spider chart or redesigned visual comparison                  | The prose table makes 5×5 comparative claims; a visual encoding reveals patterns the table obscures                      |
| 14  | "Model capability and architectural soundness are orthogonal properties"                | VG        | 2×2 quadrant diagram (model capability vs. architectural soundness)           | "Orthogonal properties" is a spatial metaphor that demands a 2D plane; prose asserts it, cannot demonstrate it           |

> **Heuristic Key:** MC = Mechanism Complexity | VG = Verification Gap | PQ = Proportional/Quantitative Data

---

## Phase 3: Full Prompt Sets

---

### Figure 1 — ReAct Loop: The Think-Act-Observe Cycle with Dual Exit Paths

**Priority: IMPORTANT**

**What this figure must show:**
The three-node cycle (Think → Act → Observe → Think) enclosed in a dashed loop boundary. Two distinct exit paths branching from the Think node: (1) the FINISH signal leading to a clean Done node; (2) the max_steps counter leading to a Force Exit node. The visual distinction between the happy path and the safety path is the figure's entire argumentative purpose.

**What the failure path must look like:**
Not applicable to this figure — this is the working architecture. The failure mode (infinite loop from removing max_steps) is addressed in the causal chain figure below.

**What a reader must be able to answer from this figure alone:**
_"What stops the ReAct loop? Where do both exits live? What is the difference between the happy path and the safety path?"_

**Recommended figure type:** Looped cycle flowchart with annotated exit conditions

---

#### Component A — Structural Prompt

> "Generate a cycle flowchart showing the ReAct Think-Act-Observe loop. Include three primary nodes in a vertical cycle: Think (reasoning trace), Act (tool call), Observe (environment response). Show a feedback arrow from Observe back up to Think. Show two exit conditions branching from the Think node: (1) a FINISH signal leading to a Done / Return Answer node; (2) a max_steps counter leading to a Force Exit / Best Answer node. Enclose the three-node cycle in a dashed boundary labeled 'ReAct loop (bounded by max_steps).' Label all arrows. Style: clean academic line diagram, white background, no decorative elements."

#### Component B — Aesthetic Prompt

> "Three-node reasoning cycle diagram, vertical loop arrangement, purple node for internal reasoning, teal nodes for external interaction, green done exit, amber safety exit, dashed boundary enclosing the loop, directional arrows, flat vector, slate blue and warm amber palette, diffuse lighting, centered composition, technical diagram, peer-review quality --v 6.1 --style raw --stylize 50 --no cinematic, vibrant, glow, neon, bokeh, plastic, 3D render artifacts, watercolor, collage"

#### Component C — Verification Checklist

- [ ] Two distinct exit paths (FINISH signal and max_steps) are visually separate
- [ ] Loop boundary is visually distinct from exit nodes
- [ ] Directional arrows make cycle direction unambiguous
- [ ] Color palette distinguishes internal reasoning nodes from external interaction nodes
- [ ] No 3D perspective distortion
- [ ] Legend present distinguishing the two exit node types

---

### Figure 2 — Plan-and-Execute: The Stale Plan Failure Mode

**Priority: CRITICAL**

**What this figure must show:**
A horizontal timeline with four timestamps (T=0 through T=3). The Planner creates a plan at T=0 with a stated assumption (Schema v1). The Executor proceeds at T=1. A World Change event (Schema → v2) occurs at T=2. The Executor at T=3 still applies the T=0 assumption. A red dashed propagation arrow connects the stale assumption across the timeline to the output. A final node labeled "structurally valid, semantically wrong — no exception raised."

**What the failure path must look like:**
The divergence zone (T=2 onward) should be shaded to make plan-world separation visible. The stale propagation arrow should be visually distinct from normal flow arrows — dashed, red, crossing the timeline. The output node should not look like an error state (it looks like success — that is the danger).

**What a reader must be able to answer from this figure alone:**
_"At what point does the plan go stale? Why doesn't the system catch it? What reaches the output?"_

**Recommended figure type:** Horizontal timeline divergence diagram with causal propagation arrow

---

#### Component A — Structural Prompt

> "Generate a timeline diagram showing the Plan-and-Execute stale plan failure mode. Show a horizontal time axis with four timestamps: T=0, T=1, T=2, T=3. At T=0, show a Planner node creating a plan with a stated assumption (Schema v1). At T=1, show an Executor node completing Step 1 successfully. At T=2, show a World Change event node (Schema → v2) in red. At T=3, show the Executor still using Schema v1 assumptions. Draw a red dashed arrow from the T=0 plan assumption curving across to T=3 execution, labeled 'stale assumption propagates silently.' Show a final output node labeled 'structurally valid, semantically wrong — no exception raised.' Shade the T=2 to T=3 region as a divergence zone. Style: clean academic line diagram, white background."

#### Component B — Aesthetic Prompt

> "Horizontal timeline divergence diagram, four timestamp markers, purple planner node, teal executor nodes, red world-change event node, amber divergence zone shading, red dashed propagation arrow crossing the timeline, flat vector, slate and red palette, diffuse lighting, centered composition, technical diagram, peer-review quality --v 6.1 --style raw --stylize 50 --no cinematic, glow, neon, 3D render artifacts"

#### Component C — Verification Checklist

- [ ] Timeline direction is unambiguous (left = earlier, right = later)
- [ ] Divergence zone is visually distinct from the normal execution region
- [ ] Stale propagation arrow is distinct from normal flow arrows (dashed, different color)
- [ ] Silent failure is annotated ("no exception raised")
- [ ] Output node does not visually resemble an error — it should look like a normal output
- [ ] Color differentiates healthy state from failure state

---

### Figure 3 — Reflection Pattern: Convergence vs. Oscillation

**Priority: CRITICAL**

**What this figure must show:**
Two side-by-side line charts, same axes and scale. Left chart: critic scores rising monotonically from ~0.52 to ~0.91 across 6 rounds, crossing a dashed threshold line at 0.85 — labeled "Coherent criteria — convergence." Right chart: critic scores alternating between ~0.60 and ~0.80 for 8 rounds, never crossing the threshold — labeled "Contradictory criteria — oscillation." Both charts share the same threshold line so the comparison is direct.

**What the failure path must look like:**
The oscillating pattern on the right must be visually unambiguous: regular alternation, no net improvement, always below threshold. Ideally the right chart uses red for the line to contrast with the left chart's blue.

**What a reader must be able to answer from this figure alone:**
_"How do I know if my reflection loop has contradictory criteria? What does the score trace look like when it works vs. when it fails? Why is 'more rounds' not the fix?"_

**Recommended figure type:** Side-by-side convergence line charts with shared threshold annotation

---

#### Component A — Structural Prompt

> "Generate two side-by-side line charts, each showing Critic Score (y-axis, 0.0–1.0) vs. Round Number (x-axis, 1–8). Left chart: scores rise monotonically from approximately 0.52 to 0.91, crossing a horizontal dashed threshold line at 0.85 by round 5. Label this 'Coherent criteria — convergence.' Right chart: scores alternate between approximately 0.60 and 0.80 for all 8 rounds, never crossing the 0.85 threshold line. Label this 'Contradictory criteria — oscillation.' Use blue for the left line, red for the right line. Add a caption below: 'Oscillating scores are the diagnostic signature of contradictory criteria — the fix is criteria revision, not more rounds.' Style: clean academic chart, white background, minimal gridlines."

#### Component B — Aesthetic Prompt

> "Two side-by-side convergence charts, critic score vs. round number, blue monotonic convergence curve left panel, red oscillating sawtooth curve right panel, shared dashed green threshold line at 0.85 on both panels, same y-axis scale both charts, flat design, clean axis labels, academic paper style, diffuse lighting --v 6.1 --style raw --stylize 50 --no cinematic, glow, neon, 3D render artifacts, decorative backgrounds"

#### Component C — Verification Checklist

- [ ] Y-axis starts at zero on both charts
- [ ] Threshold line is visible and identical on both charts
- [ ] Both convergence and oscillation patterns are visually unambiguous
- [ ] Both charts use the same y-axis scale so direct comparison is valid
- [ ] Color palette is colorblind-accessible (supplement with line style if needed — solid vs. dashed)
- [ ] Caption explains the diagnostic implication
- [ ] Data source cited (illustrative, not empirical — note this in caption)

---

### Figure 4 — Multi-Agent Topology: Architecture and the Deadlock Failure Mode

**Priority: CRITICAL**

**What this figure must show:**
One Orchestrator node at top. Three Specialist nodes below (Researcher, Writer, Reviewer) connected to a horizontal shared message bus. Normal handoff flow arrows: Researcher → Writer → Reviewer. Then: the deadlock state — two opposing red dashed circular arrows between Writer and Reviewer, each labeled "awaiting output from." The Writer-Reviewer pair enclosed in a red dashed boundary labeled "circular wait — deadlock." The Orchestrator visually positioned as a router, not an executor.

**What the failure path must look like:**
The circular arrows between Writer and Reviewer should be the most visually salient element — heavier weight, red, bidirectional. The normal flow arrows should recede. A reader should be able to see immediately that the two agents are waiting for each other and neither will proceed.

**What a reader must be able to answer from this figure alone:**
_"What is a coordination deadlock? How does it differ from a single agent timeout? Where in this system would it appear? What makes it distinct from the Orchestrator failing?"_

**Recommended figure type:** Network topology diagram with overlaid failure state annotation

---

#### Component A — Structural Prompt

> "Generate a topology diagram showing a multi-agent system. Place one Orchestrator node at top center. Below it, draw a horizontal shared message bus (dashed rectangle, labeled 'shared message bus'). Below the bus, place three Specialist nodes side by side: Researcher, Writer, Reviewer. Draw normal vertical connection lines from bus to each specialist. Show handoff flow arrows along the bus from Researcher to Writer to Reviewer. Then overlay the deadlock state: draw two opposing red dashed arrows between Writer and Reviewer, each pointing toward the other, labeled 'awaiting response from.' Enclose the Writer-Reviewer pair in a red dashed boundary labeled 'circular wait.' Include a legend: specialist agents, orchestrator, normal flow, circular wait. Style: clean academic line diagram, white background."

#### Component B — Aesthetic Prompt

> "Multi-agent coordination topology diagram, orchestrator at top, three specialist nodes on shared dashed message bus, purple orchestrator node, teal specialist nodes, red dashed bidirectional deadlock arrows between two agents, red dashed enclosure around deadlocked pair, normal flow arrows in gray, flat vector, slate and red palette, diffuse lighting, centered composition, technical diagram, peer-review quality --v 6.1 --style raw --stylize 50 --no cinematic, glow, neon, 3D render artifacts"

#### Component C — Verification Checklist

- [ ] Message bus is visually distinct from agent nodes
- [ ] Normal flow arrows and deadlock arrows are visually distinct (color + line style)
- [ ] Deadlock pair is enclosed and labeled
- [ ] Orchestrator's non-executing role is indicated (routes, doesn't act on subtasks)
- [ ] Bidirectional nature of deadlock is unambiguous
- [ ] Legend present and complete
- [ ] No 3D perspective distortion

---

### Figure 5 — Memory-Augmented Architecture and Context Poisoning

**Priority: IMPORTANT**

**What this figure must show:**
Two memory stores: Short-term (current session, context window) and Long-term (AGENT_MEMORY external table). A Retrieval Layer between the long-term store and the Agent node. The Agent generating output. The write path from Agent output through a Validation Check node back to the long-term store. One record in the long-term store highlighted as "poisoned (is_poisoned = TRUE)." A red dashed arrow from the poisoned record through the retrieval layer to the Agent, labeled "retrieved as ground truth." The Agent producing a "fluent, confident, wrong answer" output.

**What the failure path must look like:**
The contamination path (poisoned record → retrieval → agent → wrong output) should be visually continuous and red. The validation check on the write path should be marked as the absent defense — either grayed out, marked "often omitted," or shown as a bypass arrow. The output node should not look like an error — it should look like successful output (because it is, superficially).

**What a reader must be able to answer from this figure alone:**
_"Where does a poisoned memory enter the system? Why doesn't the agent know the memory is wrong? What architectural component is the defense? Why is this failure invisible to the end user?"_

**Recommended figure type:** Architecture flow diagram with contamination path overlay

---

#### Component A — Structural Prompt

> "Generate an architecture diagram showing a memory-augmented agent system. Include: Short-term memory node (current session), Long-term store node (AGENT_MEMORY external table), Retrieval Layer node (keyword matching), Agent node (generates response), Output node (answer). Show normal flow: short-term memory + retrieved long-term memories → Agent → Output. Show write path: Agent output → Validation Check → Long-term store. Highlight one record in the long-term store as 'poisoned (is_poisoned = TRUE)' in red. Draw a red dashed arrow from the poisoned record through the retrieval layer to the agent, labeled 'retrieved as ground truth.' Show the output as 'fluent, confident, wrong answer.' Mark the validation check as absent or bypassed in most implementations. Style: clean academic architecture diagram, white background."

#### Component B — Aesthetic Prompt

> "Memory-augmented agent architecture diagram, purple short-term memory node, blue long-term store node with one red poisoned record, gray retrieval layer node, purple agent node, amber wrong-output node, green validation gate marked as absent, red dashed contamination path from poisoned record through retrieval to agent to output, flat vector, slate and red palette, diffuse lighting, left-to-right layout, technical diagram, peer-review quality --v 6.1 --style raw --stylize 50 --no cinematic, glow, 3D render artifacts"

#### Component C — Verification Checklist

- [ ] Two memory stores are visually distinct from each other
- [ ] Retrieval layer is clearly positioned between long-term store and agent
- [ ] Poisoned record is visually differentiated from valid records
- [ ] Write path (validation) is visually separate from read path (retrieval)
- [ ] Contamination path is distinct from normal flow (color + line style)
- [ ] Output node does not resemble an error state
- [ ] Validation check is annotated as the missing defense
- [ ] Legend present

---

### Figure 6 — Pattern Selection Decision Tree

**Priority: IMPORTANT**

**What this figure must show:**
A top-down binary decision tree. Root node: "New task." Five levels, each with one yes/no diagnostic question matching the chapter's five criteria exactly. Yes exits go right to a terminal pattern node. No exits continue downward. Five terminal nodes: Plan-and-Execute, ReAct, Reflection, Multi-Agent, Memory-Augmented — each distinctly colored. A default terminal at the bottom of the No chain: "Start with simplest pattern."

**What the failure path must look like:**
Not applicable — this is a decision aid, not a failure diagram.

**What a reader must be able to answer from this figure alone:**
_"Given any task description, which pattern do I reach? What question eliminates each pattern? Can two patterns ever be reached by the same task? Where do I start if nothing applies?"_

**Recommended figure type:** Top-down binary decision tree with colored terminal nodes

---

#### Component A — Structural Prompt

> "Generate a top-down decision tree flowchart. Root node: 'New task.' Each level has one rounded-rect question node. Q1: 'Stable ordered subtasks?' — Yes (right) → Plan-and-Execute terminal. Q2: 'Dynamic tool use, real-time results?' — Yes (right) → ReAct terminal. Q3: 'Verifiable quality criteria exist?' — Yes (right) → Reflection terminal. Q4: 'Multiple distinct domains?' — Yes (right) → Multi-Agent terminal. Q5: 'Cross-session context needed?' — Yes (right) → Memory-Augmented terminal. No from Q5 → 'Start with simplest pattern' terminal. All No exits go downward. Label Yes and No on all branching arrows. Each pattern terminal node uses a distinct color. Style: clean academic flowchart, white background."

#### Component B — Aesthetic Prompt

> "Five-level binary decision tree, yes exits right to colored pattern terminal nodes, no exits downward, gray neutral question nodes, five distinctly colored terminal pattern nodes, yes and no labels on all arrows, directional flow arrows, flat vector, academic clean style, diffuse lighting, centered top-down composition, technical diagram, peer-review quality --v 6.1 --style raw --stylize 50 --no cinematic, glow, decorative, 3D render artifacts"

#### Component C — Verification Checklist

- [ ] All five patterns appear as terminal nodes
- [ ] Yes/No labels are present on all branching arrows
- [ ] Flow direction is unambiguous (top to bottom, yes exits right)
- [ ] Decision criteria match the chapter's five diagnostic questions exactly — no paraphrasing
- [ ] No pattern is reachable by two paths (exits are mutually exclusive)
- [ ] Default terminal ("start simple") is present at the bottom of the No chain
- [ ] Color palette is colorblind-accessible (supplement with shape or label if needed)

---

### Figure 7 — The Orthogonality Claim: Model Capability vs. Architectural Soundness

**Priority: IMPORTANT**

**What this figure must show:**
A 2×2 quadrant diagram. X-axis: "Model capability →". Y-axis: "Architectural soundness →". Four labeled quadrants: Bottom-left "Breaks quietly" (low/low). Top-left "Constrained and safe" (high architecture, low model). Bottom-right "Breaks convincingly" (high model, low architecture) — this is the danger zone, red-tinted. Top-right "Reliable" (high/high) — the target state, green-tinted. In the bottom-right (danger) quadrant: three example points labeled "ReAct without loop limit," "Reflection with bad criteria," "Memory without validation." Caption: "Improving model capability does not compensate for architectural deficiency."

**What the failure path must look like:**
The bottom-right quadrant must be the most salient — it is the counter-intuitive danger zone. A reader should be able to see at a glance that "smarter model + bad architecture" is worse than "weak model + good architecture" because the output is more convincing.

**What a reader must be able to answer from this figure alone:**
_"Can a smarter model compensate for a missing loop limit? Which quadrant represents the worst failure mode? Where do the chapter's three worst failure cases land?"_

**Recommended figure type:** 2×2 quadrant diagram with annotated failure examples

---

#### Component A — Structural Prompt

> "Generate a 2×2 quadrant diagram. X-axis label: 'Model capability →'. Y-axis label: 'Architectural soundness →'. Label four quadrants: bottom-left 'Breaks quietly' (weak model, weak architecture); top-left 'Constrained and safe' (weak model, strong architecture); bottom-right 'Breaks convincingly — danger zone' (strong model, weak architecture), tinted red; top-right 'Reliable — target state' (strong model, strong architecture), tinted green. In the bottom-right quadrant, place three labeled example points: 'ReAct without loop limit,' 'Reflection with bad criteria,' 'Memory without validation.' Add caption: 'Improving model capability does not compensate for architectural deficiency.' Style: clean academic diagram, white background."

#### Component B — Aesthetic Prompt

> "2x2 orthogonality quadrant diagram, model capability x-axis, architectural soundness y-axis, red-tinted danger zone bottom-right quadrant, green-tinted target state top-right quadrant, three labeled failure example points in danger quadrant, neutral gray other two quadrants, directional axis arrows, flat vector, academic style, diffuse lighting, centered composition, technical diagram, peer-review quality --v 6.1 --style raw --stylize 50 --no cinematic, glow, decorative, 3D render artifacts"

#### Component C — Verification Checklist

- [ ] Both axes are labeled with direction arrows
- [ ] All four quadrants are distinctly labeled
- [ ] Danger quadrant (high model, low architecture) is visually distinct and most prominent
- [ ] Target quadrant (high model, high architecture) is positively marked
- [ ] Three failure examples appear in the correct quadrant
- [ ] Caption states the orthogonality claim explicitly
- [ ] No 3D distortion
- [ ] Color tints are accessible (supplement with pattern fill for print)

---

## Phase 4: Density Recommendation

For this text, I recommend **7 figures** using **Mechanistic density** — one figure per major architectural claim, following a strict Structure → Failure Mode pipeline. The breakdown by figure type is:

- **Topology/mechanism diagrams:** Figures 1, 4, 5
- **Temporal/causal diagrams:** Figure 2
- **Quantitative/convergence charts:** Figure 3
- **Decision aid:** Figure 6
- **Argumentative/conceptual:** Figure 7

Every figure is renderable as a publication-quality static image or as an interactive digital-first version. The interactive priority order is: Figure 3 (live score plotting), Figure 1 (step-through animation of the loop), Figure 6 (interactive tree navigation).

---

## Phase 5: Priority Ranking

> The Hero Image is mandatory infrastructure and ranked separately from all analytical figures.

| Rank | Figure                                   | Priority      | Rationale                                                                                                                                                                                                                                       |
| ---- | ---------------------------------------- | ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | Fig. 3 — Reflection Oscillation Chart    | **CRITICAL**  | The oscillation signature is the chapter's only quantitative claim. "Scores alternate between two values" is unverifiable without a chart. Readers debugging reflection loops need this exact diagnostic pattern.                               |
| 2    | Fig. 2 — Stale Plan Timeline             | **CRITICAL**  | "Silent failure" is the chapter's highest-risk claim. The T=0/T=2 divergence is a temporal architecture concept that prose cannot make spatial. Without this figure, readers cannot trace _why_ the output looks correct while being wrong.     |
| 3    | Fig. 4 — Multi-Agent Topology + Deadlock | **CRITICAL**  | Deadlock is definitionally a topological concept (circular dependency). Describing it in prose without a diagram is the single highest-risk zone for the Eddy audit — the causal chain is asserted but not demonstrated.                        |
| 4    | Fig. 1 — ReAct Cycle Diagram             | **IMPORTANT** | The three-step cycle with dual exits is the chapter's foundational mechanism. Without it, readers absorb the code block but not the architectural intent. The `max_steps` vs. `FINISH` distinction is crucial and visually non-obvious.         |
| 5    | Fig. 5 — Memory Architecture + Poisoning | **IMPORTANT** | The dual-store design with a retrieval layer is a 4-component architecture claim. Context poisoning's "invisible" quality is the point — the diagram makes the path of corruption visible in a way prose cannot.                                |
| 6    | Fig. 6 — Pattern Selection Tree          | **IMPORTANT** | The 5-question diagnostic is written as prose paragraphs, which buries the branching structure. A reader using this chapter as a reference (not reading linearly) needs the tree to navigate quickly.                                           |
| 7    | Fig. 7 — Capability vs. Architecture 2×2 | **IMPORTANT** | "Orthogonal properties" is a strong argumentative claim at the chapter's climax. The quadrant diagram converts an abstract philosophical assertion into a verifiable spatial claim — and places the failure examples exactly where they belong. |

---

## ⚠ Eddy the Editor: High-Risk Unsupported Claim Audit

The following sections make architectural claims with **no supporting mechanism** — the zones most vulnerable to editorial challenge.

---

### Risk Zone 1 — "The model has no concept of 'enough.' It generates the next token. That is all it does."

**Location:** Introduction, "The Illusion of the Smart Agent"

**Risk level:** HIGH — This is the chapter's foundational claim and it receives no mechanism diagram.

**Gap:** A figure showing token generation as a stateless, next-prediction operation (versus a stopping criterion as an external architectural gate) would make this undeniable rather than assertable. As written, readers are asked to accept the claim on the author's authority.

**Recommended addition:** A minimal two-panel illustration — left panel shows the token generation loop with no stopping criterion; right panel shows the same loop with an external architectural wall. Even a simple annotated diagram would close this gap.

---

### Risk Zone 2 — "The separation between planner and executor is the core architectural idea."

**Location:** Pattern 2, Mechanism section

**Risk level:** MEDIUM-HIGH — The prose asserts the separation is important but never diagrams what "separation" means structurally.

**Gap:** Figure 2 (rendered above) addresses the failure mode but not the normal-state architecture. A side-by-side showing "single agent with full goal context" versus "separated planner + executor with task handoff" would justify the architectural choice rather than merely state it.

**Recommended addition:** A two-panel comparison — monolithic agent vs. separated planner/executor — with annotations showing where each loses track of context.

---

### Risk Zone 3 — "The quality of the Critic's criteria is therefore the determining factor in the pattern's effectiveness — not the quality of the Generator."

**Location:** Pattern 3, Mechanism section

**Risk level:** HIGH — This is a strong, counterintuitive claim that is asserted without comparison data or mechanism.

**Gap:** An ablation-style figure (same model, different criteria quality → different convergence outcomes) would make this credible rather than memorable. The claim directly contradicts the intuition that "better model = better output" — which is exactly the chapter's thesis — but the Reflection section is where the thesis needs its sharpest empirical support.

**Recommended addition:** A three-panel convergence chart: (1) weak model + coherent criteria → converges; (2) strong model + contradictory criteria → oscillates; (3) strong model + coherent criteria → converges fastest. This single figure would carry more argumentative weight than any paragraph.

---

### Risk Zone 4 — "The Orchestrator does not execute tasks itself. It routes, monitors, and assembles."

**Location:** Pattern 4, Mechanism section

**Risk level:** MEDIUM — The topology figure (Fig. 4) does not sufficiently show _what_ the Orchestrator does vs. doesn't do; it shows routing but not the distinction from execution.

**Gap:** A sequence diagram showing the Orchestrator's message flow — receive goal, decompose, route to Researcher, receive output, route to Writer, receive output, assemble final — with an explicit annotation "Orchestrator never calls external tools directly" would close this gap.

**Recommended addition:** A narrow sequence diagram alongside or below the topology figure, showing one complete pass of the pipeline from the Orchestrator's perspective only.

---

### Risk Zone 5 — "Model capability and architectural soundness are orthogonal properties. Improving one does not compensate for deficiencies in the other."

**Location:** Closing section, "The Architecture Is the Argument"

**Risk level:** HIGH — This is the chapter's thesis statement and receives one paragraph of rhetorical support.

**Gap:** The quadrant diagram (Fig. 7) partially addresses this, but the claim needs an empirical grounding note or citation to be audit-proof. As written, "orthogonal" is used metaphorically (they are not mathematically orthogonal in the statistical sense). If an editor challenges this claim, there is no evidence to point to beyond the failure examples described in the chapter itself.

**Recommended addition:** A footnote or parenthetical noting that "orthogonal" is used in the sense of "independently varying" — the claim is that holding one constant does not constrain the other. Optionally, cite the Reflexion paper (Shinn et al., 2023) or the AutoGen paper (Wu et al., 2023) for empirical cases where strong models failed architecturally.

---

_Document generated by the Figure Architect system for publication-quality figure planning._
_Chapter: "Five Patterns, Five Trade-offs" | Book: Design of Agentic Systems with Case Studies_
