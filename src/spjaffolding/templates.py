import textwrap


def generate_pyproject_toml(tool_name: str, description: str) -> str:
    """Generates the modified pyproject.toml adhering to PEP 621/735."""
    return textwrap.dedent(f"""\
        [project]
        name = "{tool_name}"
        version = "0.1.0"
        description = "{description}"
        readme = "README.md"
        requires-python = ">=3.10"
        dependencies = []

        [project.scripts]
        {tool_name} = "{tool_name}.cli:app"

        [project.optional-dependencies]
        gpu = ["torch", "xgboost"]
        viz = ["matplotlib", "seaborn"]
        test = ["pytest", "ruff", "mypy"]
        
        [build-system]
        requires = ["hatchling"]
        build-backend = "hatchling.build"
    """)


def generate_cli_py(tool_name: str) -> str:
    """Generates the main entry point leveraging argparse/typer for mode chaining."""
    return textwrap.dedent(f"""\
        import argparse
        import sys
        from pathlib import Path

        def execute_mode(mode: str, workspace_path: Path, options: str) -> None:
            \"\"\"Executes a single mode of the state machine.\"\"\"
            print(f"Executing mode: {{mode}} in {{workspace_path}} with options: {{options}}")
            # Logic implementation per mode goes here

        def app() -> None:
            parser = argparse.ArgumentParser(description="{tool_name} Execution Engine")
            
            parser.add_argument(
                "-m", "--mode",
                required=True,
                help="Execution state or chain of states (e.g., convert_csv_prepare_inputs_train)"
            )
            parser.add_argument(
                "-p", "--project-path",
                nargs=2,
                metavar=("WORKSPACE", "PROJECT"),
                required=True,
                help="Two-string array <WORKSPACE> <PROJECT> routing to specific data directory."
            )
            parser.add_argument(
                "-o", "--options",
                default="",
                help="String for granular directives."
            )
            
            args = parser.parse_args()
            
            # Resolve workspace target
            root_workspace = Path("workspaces").resolve()
            target_workspace = root_workspace / args.project_path[0] / args.project_path[1]
            target_workspace.mkdir(parents=True, exist_ok=True)
            
            modes_to_run = [m.strip() for m in args.mode.split("_")]
            
            for mode in modes_to_run:
                execute_mode(mode, target_workspace, args.options)

        if __name__ == "__main__":
            app()
    """)


def generate_init_py() -> str:
    """Generates a blank __init__.py."""
    return ""
