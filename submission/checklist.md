# Pre-Submission Checklist

<!-- Verify each item before submitting -->

- [x] Chapter prose complete in chapter/chapter04.md
- [x] Substack HTML exported to chapter/chapter04.html
- [x] Author's Note finalized (3 pages)
- [x] All figures generated and referenced (13 figures: hero + Fig 0–7 + Fig 2A, 3A, 3 Convergence, 3 Oscillation, 4A)
- [x] No credentials committed (.env is gitignored)
- [x] Notebook executed top-to-bottom (chapter04_demo_executed.ipynb committed)
- [x] All five Human Decision Nodes present in notebook (cells 7, 12, 16, 20, 24) with # MANDATORY HUMAN DECISION NODE code blocks in failure cells (8, 13, 17, 21, 25)
- [x] Failure modes trigger and log correctly (LoopLimitError, stale plan, OscillationError, DeadlockError, context poisoning)
- [ ] Snowflake setup.sql runs without errors on a fresh account (verify manually before submission)
- [x] Mermaid diagrams render correctly in final HTML (chapter04.html uses pre-built PNG <img> tags — no Mermaid JS runtime needed)
- [ ] teardown.sql tested and cleans up completely (verify manually)
- [ ] Video recorded, uploaded to YouTube/Vimeo (unlisted), and link added to README (placeholder section added — paste URL into README > Video Walkthrough)
