import typer
from rich.console import Console
from enum import Enum
from spjaffolding.generator import orchestrate_generation

app = typer.Typer(help="The `spjaffolding` wizard for advanced ML tool scaffolding.")
console = Console()

class ProjectDomain(str, Enum):
    numerical_ml = "numerical_ml"
    llm_scraping = "llm_scraping"

@app.command()
def main(
    tool_name: str = typer.Option(..., prompt="tool_name (e.g., bead, phaze)"),
    description: str = typer.Option(..., prompt="description"),
    project_domain: ProjectDomain = typer.Option(
        ...,
        prompt="project_domain",
        help="A critical toggle. Expected 'numerical_ml' or 'llm_scraping'",
    ),
) -> None:
    """Entry point for scaffolding."""
    console.print(f"[bold green]Starting scaffolding for: {tool_name}[/bold green]")
    try:
        orchestrate_generation(
            tool_name=tool_name,
            description=description,
            project_domain=project_domain.value
        )
        console.print(f"[bold blue]Successfully scaffolded {tool_name}![/bold blue]")
    except Exception as e:
        console.print(f"[bold red]Generation encountered an error: {e}[/bold red]")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
