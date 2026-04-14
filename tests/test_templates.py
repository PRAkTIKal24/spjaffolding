import pytest
from spjaffolding.templates import generate_pyproject_toml, generate_cli_py, generate_init_py

def test_generate_pyproject_toml():
    toml = generate_pyproject_toml("test_tool", "A test tool description", ["gpu"])
    assert "name = \"test_tool\"" in toml
    assert "description = \"A test tool description\"" in toml
    assert "gpu = [\"torch\", \"xgboost\"]" in toml

def test_generate_cli_py():
    cli = generate_cli_py("test_tool", ["gpu"])
    assert "import argparse" in cli
    assert "def execute_mode(mode: str, workspace_path: Path, options: str) -> None:" in cli
    assert "description=\"test_tool Execution Engine\"" in cli

def test_generate_init_py():
    init = generate_init_py()
    assert init == ""

from spjaffolding.templates import (
    generate_config_py,
    generate_logger_py,
    generate_env_example,
    generate_pre_commit_yaml,
    generate_main_py,
)

def test_generate_config_py():
    config = generate_config_py()
    assert "pydantic_settings" in config

def test_generate_logger_py():
    logger = generate_logger_py()
    assert "rich.logging" in logger

def test_generate_env_example():
    env = generate_env_example()
    assert "APP_NAME" in env

def test_generate_pre_commit_yaml():
    pc = generate_pre_commit_yaml()
    assert "ruff" in pc
    assert "mypy" in pc

def test_generate_main_py():
    main = generate_main_py("my_tool")
    assert "from my_tool.cli import app" in main
