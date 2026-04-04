# Chapter 4 — Five Patterns, Five Trade-offs

Agentic Systems Book, Chapter 04 project repository.

## Project Structure

```
chapter04-five-patterns/
├── README.md
├── .env.example                    # Snowflake credentials template
├── snowflake/
│   ├── setup.sql                   # Database provisioning
│   ├── teardown.sql                # Cleanup script
│   └── queries.py                  # Python Snowflake connection layer
├── chapter/
│   ├── chapter04.md                # Main chapter prose
│   ├── chapter04.html              # Substack-ready HTML
│   └── authors_note.md             # 3-page Author's Note
├── notebook/
│   └── chapter04_demo.ipynb        # Main Jupyter demo notebook
├── figures/
│   └── figure_prompts.md           # Figure Architect prompts
├── assets/
│   └── diagrams/
│       └── all_diagrams.md         # All Mermaid diagrams
└── submission/
    └── checklist.md                # Pre-submission checklist
```

## Quick Start

1. Copy `.env.example` to `.env` and fill in your Snowflake credentials.
2. Run `snowflake/setup.sql` in your Snowflake worksheet to provision the database.
3. Open `notebook/chapter04_demo.ipynb` to run the demos.

## Teardown

Run `snowflake/teardown.sql` to drop all objects for a clean re-run.
