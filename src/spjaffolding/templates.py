import textwrap


def generate_pyproject_toml(tool_name: str, description: str, features: list[str]) -> str:
    """Generates the modified pyproject.toml adhering to PEP 621/735."""
    toml = textwrap.dedent(f"""\
        [project]
        name = "{tool_name}"
        version = "0.1.0"
        description = "{description}"
        readme = "README.md"
        requires-python = ">=3.10"
        dependencies = [
            "pydantic-settings",
            "rich"
        ]

        [project.scripts]
        {tool_name} = "{tool_name}.cli:app"

        [project.optional-dependencies]
        test = ["pytest", "ruff", "mypy"]
    """)
    
    if "gpu" in features:
        toml += 'gpu = ["torch", "xgboost"]\n'
    if "viz" in features:
        toml += 'viz = ["matplotlib", "seaborn"]\n'
    
    toml += textwrap.dedent("""\
        
        [build-system]
        requires = ["hatchling"]
        build-backend = "hatchling.build"
    """)
    return toml


def generate_cli_py(tool_name: str, features: list[str]) -> str:
    """Generates the main entry point leveraging argparse/typer for mode chaining."""
    modes_str = []
    if "data_prep" in features:
        modes_str.append("prepare")
    if "model_training" in features:
        modes_str.append("train")
    if "scraping" in features:
        modes_str.append("scrape")
    if "vector_db" in features:
        modes_str.append("embed")
    if "llm_orchestration" in features:
        modes_str.append("generate")
        
    modes_example = "_".join(modes_str) if modes_str else "mode1_mode2"
    modes_help = f"Execution state or chain of states (e.g., {modes_example})"

    return textwrap.dedent(f"""\
        import argparse
        import logging
        from pathlib import Path
        from {tool_name}.logger import setup_logging
        from {tool_name}.config import settings

        logger = logging.getLogger(__name__)

        def execute_mode(mode: str, workspace_path: Path, options: str) -> None:
            \"\"\"Executes a single mode of the state machine.\"\"\"
            logger.info(f"Executing mode: {{mode}} in {{workspace_path}} with options: {{options}}")
            # Logic implementation per mode goes here

        def app() -> None:
            setup_logging()
            logger.info(f"Starting {{settings.app_name}} (Debug: {{settings.debug}})")
            parser = argparse.ArgumentParser(description="{tool_name} Execution Engine")
            
            parser.add_argument(
                "-m", "--mode",
                required=True,
                help="{modes_help}"
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

def generate_config_py() -> str:
    """Generates the pydantic-settings config file."""
    return textwrap.dedent("""\
        from pydantic_settings import BaseSettings, SettingsConfigDict

        class Settings(BaseSettings):
            app_name: str = "My ML Framework"
            debug: bool = False
            
            model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

        settings = Settings()
    """)

def generate_logger_py() -> str:
    """Generates a rich-formatted logger configuration."""
    return textwrap.dedent("""\
        import logging
        from rich.logging import RichHandler

        def setup_logging(level: int = logging.INFO) -> None:
            logging.basicConfig(
                level=level,
                format="%(message)s",
                datefmt="[%X]",
                handlers=[RichHandler(rich_tracebacks=True, markup=True)]
            )
            # Create a base logger
            logger = logging.getLogger("app")
            logger.setLevel(level)
    """)

def generate_env_example() -> str:
    """Generates the .env.example file."""
    return textwrap.dedent("""\
        # .env.example
        APP_NAME="My ML Framework"
        DEBUG=True
    """)

def generate_pre_commit_yaml() -> str:
    """Generates the .pre-commit-config.yaml."""
    return textwrap.dedent("""\
        repos:
        -   repo: https://github.com/astral-sh/ruff-pre-commit
            rev: v0.1.5
            hooks:
            -   id: ruff
                args: [ --fix ]
            -   id: ruff-format
        -   repo: https://github.com/pre-commit/mirrors-mypy
            rev: v1.7.0
            hooks:
            -   id: mypy
                additional_dependencies: [pydantic]
    """)

def generate_main_py(tool_name: str) -> str:
    """Generates a Python execution entry point."""
    return textwrap.dedent(f"""\
        from {tool_name}.cli import app

        if __name__ == "__main__":
            app()
    """)
