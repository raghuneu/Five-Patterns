# PhotoMind video demo script (~7 minutes)

## Self-intro (0:00 - 0:20)

**Show:** Yourself on camera or your screen with the project open.

> "Hey, I'm Raghu Ram Shantha Rajamani -- grad student at Northeastern. This is PhotoMind, my final project for the prompt engineering course. The whole thing started because I kept losing track of what I was spending on groceries. Seriously -- I had dozens of receipt photos on my phone and no way to actually *ask* them anything."

---

## The iPhone fail (0:20 - 1:10)

**Show:** Open the Photos app on your iPhone (screen record or mirror to Mac).

> "Let me show you what I mean. Here's my actual phone. 53 photos -- receipts from ALDI, Trader Joe's, Chipotle, food I've been eating, some screenshots, random stuff. Real life, not a curated dataset."

**Type in iPhone Photos search:** *"ALDI receipt"*

> "Nothing. Okay."

**Type:** *"How much did I spend at ALDI?"*

> "Also nothing. It can find photos that *look like* receipts, but it can't read the numbers on them. It has no idea what $4.99 means. That's the gap."

> "Apple Photos does visual similarity. Google Photos can read text in images. But neither one can answer the questions you'd actually ask about your own life -- how much did I spend this week? Where do I shop the most? There's real information locked in these photos, and nothing on my phone lets me get at it. That bugged me enough to build something that does."

---

## What is PhotoMind + first demo (1:10 - 2:30)

**Show:** Open `http://localhost:5173` in your browser. Query tab, Quick Answer mode.

> "So here's what I built. PhotoMind analyzes a photo library with GPT-4o Vision and builds a JSON knowledge base out of it. You ask questions in plain English, you get answers with confidence scores and source photos. The stack is CrewAI, React, FastAPI, plus a reinforcement learning layer on top. But honestly, easier to just show you than explain it."

**Type:** *"How much did I spend at ALDI?"* -- click Ask.

> "Under a second. Grade A confidence. Five ALDI receipts, each with a relevance score and evidence from the OCR text. Same question my phone couldn't answer at all. That felt pretty good the first time it worked."

**Click** on a photo thumbnail to show the lightbox.

> "Click any photo -- you get the full image, the filename, relevance score, the evidence snippet that matched."

**Type:** *"Show me my electric bill"* -- click Ask.

> "Grade F. 'No matching photos found.' I don't have an electric bill in my library, and the system says so instead of guessing. This is something I care about a lot -- I'd much rather get 'I don't know' than a confident wrong answer, especially when it's about money."

**Type:** *"Which store do I shop at most?"* -- click Ask.

> "Grade A. It counted across all 53 photos and ranked stores by frequency. That's not just finding one photo -- it's pattern analysis across the whole library."

**Toggle** to Deep Reasoning. *(Don't run a query -- just show the toggle.)*

> "There's a Deep Reasoning mode too -- sends the query through the full CrewAI pipeline, three GPT-4o calls, gives you a longer narrative answer. Takes 15 to 45 seconds and costs a few cents, so I'll skip it live."

**Quick click** through Knowledge Base, Performance, and Architecture tabs.

> "Other tabs: you can browse all indexed photos with their metadata, check evaluation metrics, or look at the system architecture diagram."

---

## Architecture walkthrough (2:30 - 3:20)

> "Okay, so how does it actually work under the hood? Let me walk through the architecture."

**Show:** Open the technical report, Section 2 -- the system architecture diagram.

> "Two pipelines. Ingestion is sequential -- scan photos, run each one through GPT-4o Vision, write a structured record to the knowledge base. Each photo gets entities, OCR text, a description, image type, and a confidence score."

> "Queries go through a hierarchical crew. A Controller agent figures out what you're asking, hands it to a Knowledge Retriever that does the actual search, then an Insight Synthesizer writes the final answer."

**Show:** `src/tools/photo_knowledge_base.py` -- scroll through the file briefly.

> "This is the core file. About 990 lines. Four search strategies. Factual does entity matching and OCR text search -- that's your 'how much at ALDI' queries. Semantic does keyword overlap on descriptions -- 'show me pizza photos.' Behavioral counts patterns across the whole library -- 'which store do I shop at most.' And there's an embedding strategy with MiniLM that gets fused with factual results using Reciprocal Rank Fusion."

> "Confidence grading is A through F. If nothing matches, the system declines instead of making something up. The whole point of the RL extension is keeping that intact."

---

## RL extension (3:20 - 4:30)

> "So at this point the search worked, but I had a problem. The system was sometimes confidently returning the wrong photo. And if this is supposed to be a personal finance tool, that's not just a bad UX -- it's actively misleading. That's where the RL comes in."

**Show:** `src/rl/` directory, then `src/rl/rl_config.py` -- the reward matrix.

> "Two RL approaches. Both were required by the assignment, but I picked problems where they genuinely help."

> "First one is a contextual bandit for query routing. Thompson Sampling, UCB1, and epsilon-greedy, each choosing between the four search strategies. Context is a 396-dim feature vector -- 12 handcrafted features plus a 384-dim MiniLM embedding, clustered into 4 groups with KMeans."

> "Second is a DQN confidence calibrator. I adapted this from the LunarLander DQN we built earlier in the course -- same core algorithm, very different problem. Five actions: accept high, accept moderate, hedge, requery, and decline. The interesting one is requery -- it's non-terminal. The agent can say 'that search strategy didn't work, try another one' and re-evaluate. That's what makes the discount factor actually do something. You get real temporal credit assignment through the Bellman equation, not just single-step classification."

> "The reward matrix is the part I'm most opinionated about. It's asymmetric on purpose. Correct decline is +1.0. Silent failure -- confident but wrong -- is -1.0. Think about it: if this is a personal finance tool and you confidently tell someone the wrong dollar amount, that's worse than saying 'I'm not sure.' I wanted the system to learn that same instinct. And it does."

---

## Training + evaluation (4:30 - 5:50)

> "One thing I'm proud of here -- all the RL training runs offline. No API calls at all."

> "I built a PhotoMindSimulator that pre-computes all four search strategies on every query once, caches everything, then runs thousands of training episodes against that cache. So you can iterate on the RL without burning money on OpenAI."

**Run:** *(free -- cut to output in editing if needed)*

```bash
python -m src.main train
```

> "This trains bandits and DQN agents across 5 seeds, 4000 episodes each. Bandit converges to about 69% routing accuracy, DQN to about 0.76 average reward."

**Wait for output or cut to finished output.** Point out the summary line.

**Run:** *(free)*

```bash
python -m src.main rl-eval
```

> "98 queries across three test sets. Compares five configurations, 5 seeds each, 95% confidence intervals."

> "The number that matters: the Recommended config -- rule-based routing plus DQN -- gets 86% retrieval accuracy and a 2.8% silent failure rate. Baseline is 4.7%. The DQN cut confident-but-wrong answers by 40%."

**Run:** *(free)*

```bash
python -m src.main ablation
```

> "Seven-config ablation with Cohen's d effect sizes. Confirms the DQN is what drives the silent failure reduction. The bandit helps on ambiguous queries where keyword rules break down, but rule-based routing is already pretty strong on its own."

---

## Figures + tests (5:50 - 6:20)

**Show:** Open `viz/figures/` in Finder.

> "Two figures worth looking at."

1. `dqn_rewards.png` -- "DQN reward convergence across 5 seeds. Hits about 0.76 within 500 episodes."
2. `ablation_comparison.png` -- "The full ablation. Recommended config is on the Pareto front."

> "There are 10 figures total in the repo -- regret curves, posterior distributions, action distributions -- they're all in the report."

> "Testing: 90 unit tests across three files covering reward computation, all four search strategies, and both storage backends. All passing."

---

## Wrap-up (6:20 - 6:45)

> "So that's PhotoMind. It started with me being annoyed at my phone, and turned into a contextual bandit and a multi-step DQN plugged into a CrewAI multi-agent system with a React frontend and FastAPI backend."

> "If I had to pick one design decision that defines this project, it's the reward matrix. Confidently returning wrong financial data is worse than admitting uncertainty. I built the system around that belief, and the DQN learned to respect it. Training data stays local on my machine. AI-assisted development is disclosed in the report."

> "Code, 90 unit tests, 10 figures, and the full technical report are all in the repo. Thanks for watching."

---

## Recording checklist

**Before you hit record:**

- [ ] Run `python -m src.main train`, `rl-eval`, and `ablation` once so caches and figures exist
- [ ] Start the backend: `uvicorn api.server:app --reload`
- [ ] Start the frontend: `cd web && npm run dev`
- [ ] Open `viz/figures/` PNGs in Preview tabs for quick flipping
- [ ] Have two terminal tabs ready: one for live commands, one as backup
- [ ] iPhone Photos app open with search bar visible (or screen recording of it)

**What costs money:**

| Command | Cost |
|---------|------|
| `python -m src.main train` | Free |
| `python -m src.main rl-eval` | Free |
| `python -m src.main ablation` | Free |
| `python -m src.main eval` | Free |
| `python -m src.main query --direct "..."` | Free |
| `pytest tests/ -v` | Free |
| Deep Reasoning mode in React UI | ~$0.01-0.05 per query |
| `python -m src.main query "..."` (without --direct) | ~$0.01-0.05 per query |
| `python -m src.main ingest` (without --direct) | ~$0.05-0.10 per photo |

**Timing notes:**

- `train` takes about 2 minutes on CPU -- talk through the architecture while it runs
- `rl-eval` takes about 30 seconds
- `ablation` takes about 2 minutes
- Quick Answer queries are sub-second
- Deep Reasoning queries are 15-45 seconds
