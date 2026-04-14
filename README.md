# spjaffolding

A fast, strictly-typed Python CLI application that scaffolds advanced, highly modular Machine Learning frameworks. Designed for Principal Software Engineers and Research teams who demand robust architecture without the pollution of traditional templating engines (like Jinja). 

By leveraging Python's `Typer`, `rich`, and dynamic programmatic string injection coupled with the Rust-backed speed of `uv`, `spjaffolding` ensures deterministic environment resolution and clean, readable codebases.

## Key Features

- **Jinja-Free Static Generation**: Avoids external templating engines by utilizing localized `textwrap.dedent` blocks, keeping the scaffolding tool lintable (`ruff`) and type-checked (`mypy`).
- **Mode-Driven CLI Controller**: Generates a boilerplate script integrating an argparse/Typer Finite State Machine (FSM), natively supporting sequential chained execution (e.g., `-m convert_csv_prepare_inputs_train`).
- **Domain-Specific Taxonomies**: Adapts directory structures conditionally:
  - `numerical_ml`: Scaffolds standard HEP/CFD workflows (`data_prep/`, `models/`, `training/`).
  - `llm_scraping`: Scaffolds The CIPhR Anomaly topologies (`scraping/`, `vector_db/`, `llm_orchestration/`).
- **`uv` Environment Orchestration**: Subprocess execution of `uv init` and `uv sync` locally bypasses pip dependency hell with uncompromised lockfile reproducibility. Injecting strict dependency clusters like `gpu`, `viz`, and `test` based on PEP 621/735.

## Installation

You can install `spjaffolding` globally to bootstrap ML projects anywhere on your filesystem using `uv tool`:

```bash
uv tool install . --force
```

## Quick Start

Invoke the scaffolding wizard:

```bash
spjaffold --tool-name "phaze" --description "High Energy Physics anomaly detector" --project-domain "numerical_ml"
```

This generates the complete structural footprint:
```
phaze/
├── README.md
├── pyproject.toml
├── src/
│   └── phaze/
│       ├── __init__.py
│       ├── cli.py
│       ├── data_prep/
│       ├── models/
│       └── training/
└── workspaces/
```

Within the scaffolded framework, execute your modes sequentially:
```bash
uv run phaze -m "convert_csv_prepare_inputs_train" -p default_workspace default_project
```

## Developer Guide

`spjaffolding` itself maintains high structural integrity. Check its code standard via:
```bash
uv sync --all-extras
uv run ruff check src
uv run mypy src
uv run pytest tests
```

