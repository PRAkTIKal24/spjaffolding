[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19570800.svg)](https://doi.org/10.5281/zenodo.19570800)

![GitHub Release-date](https://img.shields.io/github/release-date-pre/PRAkTIKal24/spjaffolding?style=flat&color=blue)
![Release-version](https://img.shields.io/github/v/tag/PRAkTIKal24/spjaffolding?include_prereleases&label=latest%20release&color=blue)
![GitHub repo size](https://img.shields.io/github/repo-size/PRAkTIKal24/spjaffolding)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
![GitHub forks](https://img.shields.io/github/forks/PRAkTIKal24/spjaffolding?style=flat&color=blue)

[![Tests](https://github.com/PRAkTIKal24/spjaffolding/actions/workflows/test.yml/badge.svg?event=push)](https://github.com/PRAkTIKal24/spjaffolding/actions)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)


# spjaffolding

A fast, strictly-typed Python CLI application that scaffolds advanced, highly modular Machine Learning frameworks. Designed for Principal Software Engineers and Research teams who demand robust architecture without the pollution of traditional templating engines (like Jinja). 

By leveraging Python's `Typer`, `rich`, `questionary` and dynamic programmatic string injection coupled with the Rust-backed speed of `uv`, `spjaffolding` ensures deterministic environment resolution and clean, readable codebases.

## Key Features

- **Jinja-Free Static Generation**: Avoids external templating engines by utilizing localized `textwrap.dedent` blocks, keeping the scaffolding tool lintable (`ruff`) and type-checked (`mypy`).
- **Interactive Multi-Select CLI**: Uses a beautiful macOS-native-looking, `rich`-styled checkbox interface (via `questionary`) to let users dynamically toggle specifically the modules they need.
- **Dynamic Feature Architecture**: Additive folder structures and `pyproject.toml` dependencies based on your selections:
  - `gpu`, `viz`, `data_prep`, `model_training`, `scraping`, `vector_db`, `llm_orchestration`.
- **Reusable Presets**: Easily load preconfigured bundles like `--preset numerical_ml` or `--preset llm_scraping`. Save your own custom selections to `~/.config/spjaffolding/presets.json` for future runs, and view them anytime using `--list-presets`.
- **Mode-Driven CLI Controller**: Generates a boilerplate script integrating an argparse/Typer Finite State Machine (FSM), natively supporting sequential chained execution (e.g., `-m prepare_train_evaluate`).
- **`uv` Environment Orchestration**: Subprocess execution of `uv init` and `uv sync` locally bypasses pip dependency hell with uncompromised lockfile reproducibility. Injecting strict dependency clusters like `gpu`, `viz`, and `test` based on PEP 621/735.

## Installation

Install `spjaffolding` globally to bootstrap ML projects anywhere on your filesystem using `pip` or `uv`:

> **Note**: If you don't have `uv` installed, you can quickly install it:
> ```bash
> curl -LsSf https://astral.sh/uv/install.sh | sh
> ```

```bash
pip install spjaffolding
```
**Or**
```
uv tool install spjaffolding
```

### Install from source

If you want to install from source or develop the tool:

1. Clone the repository:
```bash
git clone https://github.com/PRAkTIKal24/spjaffolding.git
cd spjaffolding
```

2. Install using `uv tool`:
```bash
uv tool install . --force
```

## Quick Start

To view all available predefined and custom presets, formatted beautifully in your terminal:

```bash
spjaffold --list-presets
```

Invoke the scaffolding wizard to use the interactive checkbox menu:

```bash
spjaffold
```

Or, if you already know the name of your project and its description, use:

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

