# Take-Home Midterm: The Agentic Author's Mandate

## INFO 7375: Prompt Engineering for Generative AI

---

## Overview

Choose a chapter from

[https://open.substack.com/pub/agenticreinforcementlearning/p/design-of-agentic-systems-with-case
Links to an external site.](https://open.substack.com/pub/agenticreinforcementlearning/p/design-of-agentic-systems-with-case)

[https://open.substack.com/pub/agenticreinforcementlearning/p/prompt-engineering-with-llms
Links to an external site.](https://open.substack.com/pub/agenticreinforcementlearning/p/prompt-engineering-with-llms)

This midterm transitions you from a student of agentic AI to an educator and author. You are tasked with producing a high-fidelity, publication-ready chapter for the upcoming book, _Design of Agentic Systems with Case Studies._

Pick a chapter and write it — text, exercises, images, code, etc.

You will use the following tools to guide your development:

- **Bookie the Bookmaker** — to draft prose that bridges the gap between high-level architectural decisions and low-level system mechanisms. [https://claude.ai/project/019c969f-482f-761c-817d-a18345a63f8b
  Links to an external site.](https://claude.ai/project/019c969f-482f-761c-817d-a18345a63f8b)
- **Eddy the Editor** — to audit your work against rigorous pedagogical standards, ensuring you aren't just replacing thinking with AI. [https://claude.ai/project/019c9699-7769-75c5-a758-014eeb8769f8
  Links to an external site.](https://claude.ai/project/019c9699-7769-75c5-a758-014eeb8769f8)
- **Figure Architect** — to generate publication-quality figure prompts for every high-assertion zone in your chapter. [https://claude.ai/project/019c7944-e1b3-76af-9b8d-a16223319f4d
  Links to an external site.](https://claude.ai/project/019c7944-e1b3-76af-9b8d-a16223319f4d)

---

## Core Requirements

### 1. Concept Selection (The Chapter)

Select one chapter from _Design of Agentic Systems with Case Studies._ Your chapter may cover an architectural pattern, a production case study, a framework or tool evaluation, a governance or risk analysis, or an operational practice. Not every chapter requires building a model. All chapters require demonstrating a failure mode.

### 2. Deliverables (The "Author's Vault")

**A. The Substack Chapter (Prose)**

- Use **Bookie** to write. Read and apply Rule #2.
- Use **Eddy the Editor** to edit. Read and apply Rule #2.
- Use **Figure Architect** to suggest figures. View and apply Rule #2.

Your chapter must make a specific architectural argument — not describe a technology. The book's master claim is: _architecture is the leverage point, not the model._ Your chapter must be a demonstrable instance of that claim.

**B. The Engine (Demo Implementation)**

A "Book-Ready" Jupyter Notebook or case deliverable, depending on your chapter type:

- **For architectural pattern, framework, or operations chapters:** A runnable implementation demonstrating the pattern, framework comparison, or operational loop. Include a deliberate failure case that shows what breaks when the design decision goes wrong.
- **For case study chapters:** A structured case analysis using `caze` or `mycaze` — corporate profile, unit economics, competitive benchmarks, three analytical questions, model answers held separately, and a one-page analytical memo stating the architectural claim, the key design decision, and what breaks if the decision is reversed.
- **For governance and risk chapters:** A threat model with a triggerable failure demonstration and a defense architecture that closes the gap.

All deliverables require:

- An **AI Scaffold** that handles one bounded enumeration task (parsing a system description, proposing agent roles, generating tool definitions) but **halts for a Mandatory Human Decision Node** before the architectural structure is finalized.
- A **failure case** that is triggered deliberately and observed — not described.

**C. The Show-and-Tell Video (10 Minutes)**

Follow the **Explain → Show → Try** structure:

- **Explain:** The architectural intuition and the design decision (2–3 mins)
- **Show:** Demo walkthrough and AI collaboration — including the Human Decision Node on camera (5–6 mins)
- **Try:** A guided exercise for the viewer to break the system (2–3 mins)

---

## The Writing & Evaluation Toolkit

To achieve a Top 25% grade, you must use these tools as co-authors:

| Tool                      | Purpose              | Key Function                                                                                                                  |
| ------------------------- | -------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **Bookie**                | Generation           | Bridges intuition to mechanism. Ensures the Tetrahedron (Structure–Logic–Implementation–Outcome) is present in every section. |
| **Eddy the Editor**       | Evaluation           | Acts as a Pedagogical Critic. Audits your draft for ABET alignment, Feynman standards, and Sycophantic AI usage.              |
| **Eddy the Storyboarder** | Video Architecture   | Generates a complete scene-by-scene CapCut storyboard from your stable chapter draft. Use before recording.                   |
| **Figure Architect**      | Visualization        | Scans for high-assertion zones and generates a prioritized suite of figure prompts.                                           |
| **Courses**               | Instructional Design | Generates Bloom's Taxonomy-compliant learning outcomes and full Show-and-Tell lesson sequences.                               |
| **Caze / MyCaze**         | Case Analysis        | Runs strategic diagnostics on real companies or generates mathematically consistent fictional cases.                          |

---

## Evaluation Criteria (100 Points Total)

### Part 1: Core Competency (80 Points)

**Architectural Rigor (35 pts):** Correct identification and explanation of the architectural pattern, failure mode, or design decision; mechanistic reasoning that traces from design choice to system behavior; the failure case is triggered and observed, not merely described.

**Technical Implementation (25 pts):** Demo handles real-world defects (missing tools, coordination failure, context overflow, latency); includes the Mandatory Human Decision Node; failure mode is triggerable by a reader who clones the repo.

**Pedagogical Clarity (20 pts):** Adherence to the Feynman Standard; engaging prose that avoids jargon-bombing; every architectural claim has a mechanism, not just a description.

### Part 2: Relative Quality (20 Points)

**Top 25%:** Your chapter is indistinguishable from a professional technical textbook. Your AI integration features a clear Human Decision Node where you explicitly rejected or corrected an AI hallucination about an architectural claim — and this moment is visible in the demo and on camera in the video.

---

## Submission Guidelines

- **GitHub Repository:** Clean code or case deliverable, professional README, and a PDF/Markdown of the chapter.
- **Pedagogical Report:** A 3-page "Author's Note" explaining your design choices, how you used the tools above, and your self-assessment.
- **Video Link:** Hosted on YouTube/Vimeo (unlisted is fine).

---

## The Recipe: A Step-by-Step Guide to Top 25%

### Before You Begin: Pick Your Chapter Honestly

Don't pick the chapter that sounds most futuristic. Pick the chapter where you can answer this question without looking anything up:

_"What breaks in this system — and why does the architecture cause the failure, not the model?"_

If you can't answer that cold, pick a different chapter.

**Classify your chapter type before Day 1 ends:**

- **Type A — Architectural Pattern:** Teaching a design decision: when to use it, what it costs, what failure mode it prevents.
- **Type B — Production Case Study:** Teaching through a real deployed system and the architectural choices it made.
- **Type C — Framework or Tool Evaluation:** Teaching how to choose — LangGraph vs. AutoGen, RAG vs. large context window, ReAct vs. Plan-and-Execute.
- **Type D — Governance or Risk Analysis:** Teaching what goes wrong and the exact causal chain from design gap to harm.
- **Type E — Operational or Production Practice:** Teaching what running this in the real world actually requires.

---

### Stage 1 — Define Your Chapter's Core Claim (Day 1)

Write this sentence before anything else:

_"After reading this chapter, a student will understand [architectural decision X] well enough to [make design choice Y] without making [mistake Z]."_

X is the design pattern, system, framework, or failure mode. Y is the decision the student can now make. Z is the specific architectural error the chapter is designed to prevent.

If you can't complete Z, you don't have a chapter. You have a Wikipedia entry.

**Run `outcomes` in Courses.** Turn your sentence into 3–5 Bloom's Taxonomy-compliant learning outcomes. These drive everything: prose sections, figures, demo structure, and video.

**The Human Decision Node lives here.** When Bookie, Courses, or Caze proposes an architectural claim or system framing — write down the one you rejected and why. That rejection is worth points.

---

### Stage 2 — Write the Chapter Prose with Bookie (Days 2–3)

The Tetrahedron for agentic chapters:

| Tetrahedron Element | Type A: Pattern                    | Type B: Case Study                   | Type C: Framework Eval                   | Type D: Risk                             | Type E: Ops                                 |
| ------------------- | ---------------------------------- | ------------------------------------ | ---------------------------------------- | ---------------------------------------- | ------------------------------------------- |
| **Structure**       | The pattern and its components     | The system and what it's made of     | The candidates                           | The threat and failure mode              | The operational loop                        |
| **Logic**           | Why this pattern over alternatives | Why these architectural choices      | The decision criteria                    | The causal chain from design to failure  | Why this practice prevents what it prevents |
| **Implementation**  | The code pattern or configuration  | The real system's specific decisions | Code for the same task in each framework | The defense architecture                 | The monitoring setup and thresholds         |
| **Outcome**         | What breaks with the wrong pattern | What the system achieves and cannot  | What you pick and what you sacrifice     | What harm the undefended system produces | What happens without this practice at scale |

Write in this order regardless of chapter type:

1. **The scenario** — one concrete situation where the design decision matters. Specific, not abstract.
2. **The mechanism** — the architectural concept itself, built from the scenario.
3. **The design decision** — what you build, configure, or choose.
4. **The failure case** — what breaks when the decision goes wrong. Not optional.
5. **The exercise** — one modification the reader can make that triggers the failure.

---

### Stage 3 — Run Figure Architect and Courses (Day 3, after stable prose draft)

**Figure Architect:** Paste your stable draft. For agentic chapters, expect it to flag: agent coordination topology claims, memory architecture claims, workflow structure claims, failure mode causal chains, and framework comparisons. Use critical-priority figures first.

**Courses `showtell`:** Run after stable prose. The output gives you the full Explain → Show → Try lesson sequence — the spine your video must follow. Know which demo you are doing before you open Eddy the Storyboarder.

---

### Stage 4 — Run Eddy the Editor's Audit (Day 4)

Ask for: Feynman Standard check, jargon-before-intuition identification, architecture-without-mechanism identification, sycophantic AI usage audit.

**What Eddy will likely find in agentic chapters:**

- A pattern named and described but not mechanistically explained
- A case that lists what the system does without explaining why the architecture makes it do that
- A framework comparison that recommends without criteria
- A failure mode described as a risk without a causal chain
- A demo described in prose instead of shown in code

Every correction documented in your Author's Note is evidence of the Human Decision Node.

---

### Stage 5 — Build the Demo or Case Deliverable (Days 4–5)

All deliverable types require an AI Scaffold with a hard stop:

python

```python
# MANDATORY HUMAN DECISION NODE
# The agent coordination structure proposed above
# assumes [X architectural condition].
# Before proceeding: verify this condition holds
# for your specific use case.
# Document your verification or rejection below:
```

**Type A/C:** Minimal working implementation with a deliberate failure case. Every design decision explained in markdown cells above the code. Runnable from a fresh clone.

**Type B:** `caze` or `mycaze` case analysis — corporate profile, unit economics, competitive benchmarks, three analytical questions, model answers held separately, one-page architectural memo. Human Decision Node: the claim Caze made that you checked against a primary source.

**Type D:** Threat model with triggerable failure demonstration and defense architecture.

**Type E:** Operational artifact (monitoring scaffold, threshold framework, evaluation pipeline) with the loop running in the demo.

---

### Stage 6 — Build the Storyboard and Record the Video (Day 6)

**Step 1:** Paste your final chapter into **Eddy the Storyboarder.** Specify 8 or 10 minutes. Confirm before recording:

- The Explain act states the architectural claim, not a topic announcement
- The Show act includes the Human Decision Node with a specific AI rejection on camera
- The Try act gives the viewer one modification that breaks the system

**Step 2: Record. Structure is fixed: Explain → Show → Try.**

- **Explain (2–3 min):** State the architectural claim. Draw the system topology or design decision by hand, on camera. Name the failure mode the design prevents. Do not read from slides.
- **Show (5–6 min):** Walk through the demo or case. When you reach the Human Decision Node — stop. Say exactly: _"The AI proposed [X]. I rejected it because [architectural reasoning]."_ Show the correction. This is the most important 30 seconds of the video.
- **Try (2–3 min):** Give the viewer the one modification. Show what breaks. Leave one open question the chapter didn't fully resolve.

---

## The Author's Note (3 Pages, One Page Each)

**Page 1 — Design Choices.** Why this chapter? What about the architectural pattern, case, or failure mode required the specific approach you took? What did you leave out, and why? Name the book's master argument and explain how your chapter makes a specific instance of it.

**Page 2 — Tool Usage.** Where did Bookie generate and where did you correct it? What did Eddy the Editor flag? What did Eddy the Storyboarder produce that you modified? What did Courses, Caze, or Figure Architect contribute? Quote the AI output and your correction. Be specific about the architectural claim that was wrong and why.

**Page 3 — Self-Assessment.** Score yourself against the rubric before submission. The one that says "the failure mode in my chapter is mechanistically correct but I could not trigger it reliably in the demo, and here is what would make it triggerable" is the one that signals architectural thinking rather than checklist completion.

---

## The Top 25% Test

Answer these five questions before you submit:

1. **Can I state the book's master argument and explain how my chapter is a specific instance of it?** If not, the chapter is a feature description, not an architectural argument.
2. **Does my chapter name a failure mode, trace the causal chain from design decision to failure, and show it triggering?** If not, the chapter teaches a happy path.
3. **Is there a visible Human Decision Node — in the demo and on camera in the video — where I overruled the AI on an architectural claim?** If not, it does not exist for the grader.
4. **Does every section have all four Tetrahedron elements?** The most commonly missing element in agentic chapters is Logic — the mechanism that connects the design decision to the observed behavior.
5. **Can my reader reproduce the failure mode I demonstrate?** If the Try exercise is "think about this," it is not an exercise.

---

## Timeline

| Day | Task                                                                                                                                                   |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1   | Pick chapter type. Write the one-sentence core claim. Run `outcomes` in Courses. Identify the failure mode. Document first AI architectural rejection. |
| 2   | Write scenario and mechanism sections in Bookie.                                                                                                       |
| 3   | Write design decision and failure case sections. Run Figure Architect. Run `showtell` in Courses.                                                      |
| 4   | Eddy the Editor audit. Revise. Begin demo or case deliverable.                                                                                         |
| 5   | Complete demo: Human Decision Node, failure case trigger, runnable deliverable.                                                                        |
| 6   | Run Eddy the Storyboarder. Record video. Write Author's Note. Final check against rubric.                                                              |
| 7   | Submit.                                                                                                                                                |

---

_Architecture is the leverage point. The model is just what executes the architecture you designed. Build the chapter that proves it._

---

**Points:** 100 **Submission:** Text entry or file upload **Due:** Apr 4 at 11:59pm
