# spjaffolding

A fast, strictly-typed Python CLI application that scaffolds advanced, highly modular Machine Learning frameworks. Designed for Principal Software Engineers and Research teams who demand robust architecture without the pollution of traditional templating engines (like Jinja). 

By leveraging Python's `Typer`, `rich`, `questionary` and dynamic programmatic string injection coupled with the Rust-backed speed of `uv`, `spjaffolding` ensures deterministic environment resolution and clean, readable codebases.

## Key Features

- **Jinja-Free Static Generation**: Avoids external templating engines by utilizing localized `textwrap.dedent` blocks, keeping the scaffolding tool lintable (`ruff`) and type-checked (`mypy`).
- **Interactive Multi-Select CLI**: Uses a beautiful macOS-native-looking, `rich`-styled checkbox interface (via `questionary`) to let users dynamically toggle specifically the modules they need.
- **Dynamic Feature Architecture**: Additive folder structures and `pyproject.toml` dependencies based on your selections:
  - `gpu`, `viz`, `data_prep`, `model_training`, `scraping`, `vector_db`, `llm_orchestration`.
- **Reusable Presets**: Easily load preconfigured bundles like `--preset numerical_ml` or `--preset llm_scraping`. Save your own custom selections to `~/.config/spjaffolding/presets.json` for future runs.
- **Mode-Driven CLI Controller**: Generates a boilerplate script integrating an argparse/Typer Finite State Machine (FSM), natively supporting sequential chained execution (e.g., `-m prepare_train_evaluate`).
- **`uv` Environment Orchestration**: Subprocess execution of `uv init` and `uv sync` locally bypasses pip dependency hell with uncompromised lockfile reproducibility. Injecting strict dependency clusters like `gpu`, `viz`, and `test` based on PEP 621/735.

## Installation

You can install `spjaffolding` globally to bootstrap ML projects anywhere on your filesystem using `uv tool`:

```bash
uv tool install . --force
```

## Quick Start

Invoke the scaffolding wizard to use the interactive checkbox menu:

```bash
spjaffold --tool-name "phaze" --description "High Energy Physics anomaly detector"
```

Or run rapidly via a built-in or custom saved preset:

```bash
spjaffold --tool-name "phaze" --description "HEP anomaly detector" --preset "numerical_ml"
```

This generates the complete structural footprint based on your toggled features (e.g., `numerical_ml` preset):
```text
phaze/
├── README.md
├── pyproject.toml
├── src/
│   └── phaze/
│       ├── __init__.py
│       ├── cli.py       <-- Automatically bound to the selected domain FSM!
│       ├── data_prep/
│       ├── models/
│       └── training/
└── workspaces/
```

Within the scaffolded framework, execute your modes sequentially:
```bash
uv run phaze -m "prepare_train" -p default_workspace default_project
```

## Developer Guide

`spjaffolding` itself maintains high structural integrity. Check its code standard via:
```bash
uv sync --all-extras
uv run ruff check src
uv run mypy src
uv run pytest tests
```

