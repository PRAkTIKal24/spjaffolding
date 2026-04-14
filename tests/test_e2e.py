import os
import subprocess
import pytest
from pathlib import Path
from spjaffolding.generator import orchestrate_generation


def test_generator_numerical_ml(tmp_path: Path):
    """Test generating a numerical ML project structurally."""
    tool_name = "test_num"
    orchestrate_generation(
        tool_name=tool_name,
        description="A mathematical ML tool",
        project_domain="numerical_ml",
        output_dir=tmp_path,
    )

    proj_dir = tmp_path / tool_name
    src_dir = proj_dir / "src" / tool_name

    assert proj_dir.exists()
    assert (proj_dir / "pyproject.toml").exists()
    assert (proj_dir / "workspaces").exists()
    assert (src_dir / "__init__.py").exists()
    assert (src_dir / "cli.py").exists()

    # Domain specific folders
    assert (src_dir / "data_prep").exists()
    assert (src_dir / "models").exists()
    assert (src_dir / "training").exists()


def test_generator_llm_scraping(tmp_path: Path):
    """Test generating an LLM scraping project structurally."""
    tool_name = "test_llm"
    orchestrate_generation(
        tool_name=tool_name,
        description="An LLM scraping tool",
        project_domain="llm_scraping",
        output_dir=tmp_path,
    )

    proj_dir = tmp_path / tool_name
    src_dir = proj_dir / "src" / tool_name

    assert proj_dir.exists()
    assert (proj_dir / "workspaces").exists()

    # Domain specific folders
    assert (src_dir / "scraping").exists()
    assert (src_dir / "vector_db").exists()
    assert (src_dir / "llm_orchestration").exists()


def test_generated_project_compliance(tmp_path: Path):
    """Ensure the generated code is compliant with our standards."""
    tool_name = "compliant_tool"
    orchestrate_generation(
        tool_name=tool_name,
        description="Must pass strictly typed checks",
        project_domain="numerical_ml",
        output_dir=tmp_path,
    )

    proj_dir = tmp_path / tool_name

    # Validate syntax via ruff
    try:
        subprocess.run(["uv", "run", "--extra", "test", "ruff", "check", "src"], cwd=proj_dir, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Ruff check failed on generated code.\nSTDOUT: {e.stdout.decode()}\nSTDERR: {e.stderr.decode()}")

    # Validate typing via mypy
    try:
        subprocess.run(["uv", "run", "--extra", "test", "mypy", "src"], cwd=proj_dir, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Mypy check failed on generated code.\n{e.stdout.decode()}")


def test_generated_cli_fsm(tmp_path: Path):
    """Test that the generated CLI's entrypoint parses modes properly."""
    tool_name = "fsm_tool"
    orchestrate_generation(
        tool_name=tool_name,
        description="Test FSM mode chaining",
        project_domain="numerical_ml",
        output_dir=tmp_path,
    )
    
    proj_dir = tmp_path / tool_name

    # Execute the compiled CLI via `uv run`
    try:
        # Pass modes and the workspace project path
        result = subprocess.run(
            ["uv", "run", tool_name, "-m", "convertcsv_prepareinputs_train", "-p", "default_workspace", "default_proj"],
            cwd=proj_dir,
            check=True,
            capture_output=True,
            text=True
        )
        
        # It should print 3 mode executions based on our CLI template separated by '_'
        assert "Executing mode: convertcsv" in result.stdout
        assert "Executing mode: prepareinputs" in result.stdout
        assert "Executing mode: train" in result.stdout
        
        # Verify the target footprint inside workspaces
        target_ws: Path = proj_dir / "workspaces" / "default_workspace" / "default_proj"
        assert target_ws.exists() and target_ws.is_dir()
        
    except subprocess.CalledProcessError as e:
        pytest.fail(f"FSM CLI execution failed.\n{e.stderr}")
