# Pre-Submission Checklist

<!-- Verify each item before submitting -->

- [x] Chapter prose complete in chapter/chapter04.md
- [x] Substack HTML exported to chapter/chapter04.html
- [x] Author's Note finalized (3 pages)
- [x] All figures generated and referenced (13 figures: hero + Fig 0–7 + Fig 2A, 3A, 3 Convergence, 3 Oscillation, 4A)
- [x] No credentials committed (.env is gitignored)
- [x] Notebook executed top-to-bottom (chapter04_demo_executed.ipynb committed)
- [x] All five Human Decision Nodes present in notebook (markdown cells 12, 18, 24, 31, 37 + code cells 13, 19, 25, 32, 38), plus the AI Scaffold HDN (cells 5–6)
- [x] Failure modes trigger and log correctly (LoopLimitError, stale plan, OscillationError, DeadlockError, context poisoning)
- [x] Snowflake setup.sql runs without errors on a fresh account (verified: teardown + setup + smoke test passed)
- [x] Mermaid diagrams render correctly in final HTML (chapter04.html uses pre-built PNG <img> tags — no Mermaid JS runtime needed)
- [x] teardown.sql tested and cleans up completely (verified: teardown ran, setup re-provisioned cleanly)
- [x] Video recorded, uploaded to YouTube/Vimeo (unlisted), and link added to README (https://youtu.be/1CbxP8GUIPk)
