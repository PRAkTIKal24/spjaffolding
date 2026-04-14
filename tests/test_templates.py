import pytest
from spjaffolding.templates import generate_pyproject_toml, generate_cli_py, generate_init_py

def test_generate_pyproject_toml():
    toml = generate_pyproject_toml("test_tool", "A test tool description")
    assert "name = \"test_tool\"" in toml
    assert "description = \"A test tool description\"" in toml
    assert "gpu = [\"torch\", \"xgboost\"]" in toml

def test_generate_cli_py():
    cli = generate_cli_py("test_tool")
    assert "import argparse" in cli
    assert "def execute_mode(mode: str, workspace_path: Path, options: str) -> None:" in cli
    assert "description=\"test_tool Execution Engine\"" in cli

def test_generate_init_py():
    init = generate_init_py()
    assert init == ""
