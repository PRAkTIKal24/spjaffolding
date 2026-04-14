import json
from pathlib import Path
from typing import Optional
import typer
import questionary
from questionary import Style
from rich.console import Console
from spjaffolding.generator import orchestrate_generation

app = typer.Typer(help="The `spjaffolding` wizard for advanced ML tool scaffolding.")
console = Console()

DEFAULT_PRESETS = {
    "numerical_ml": ["gpu", "viz", "data_prep", "model_training"],
    "llm_scraping": ["scraping", "vector_db", "llm_orchestration"],
}

AVAILABLE_FEATURES = [
    questionary.Choice("🖥️  GPU / Hardware Acceleration (torch, cuml)", value="gpu"),
    questionary.Choice("📊 Data Visualization (matplotlib, seaborn)", value="viz"),
    questionary.Choice("🧹 Data Preparation Pipeline (creates data_prep/)", value="data_prep"),
    questionary.Choice("🧠 Model Training (creates models/ & training/)", value="model_training"),
    questionary.Choice("🕸️  Web Scraping (creates scraping/)", value="scraping"),
    questionary.Choice("🗄️  Vector Database / RAG (creates vector_db/)", value="vector_db"),
    questionary.Choice("🤖 LLM Orchestration (creates llm_orchestration/)", value="llm_orchestration"),
]

CUSTOM_STYLE = Style([
    ("qmark", "fg:#00ff00 bold"),
    ("question", "bold"),
    ("answer", "fg:#00ff00 bold"),
    ("pointer", "fg:#00ff00 bold"),
    ("selected", "fg:#0000ff bold"),
])

def load_presets() -> dict[str, list[str]]:
    presets = dict(DEFAULT_PRESETS)
    config_dir = Path.home() / ".config" / "spjaffolding"
    presets_file = config_dir / "presets.json"
    if presets_file.exists():
        try:
            with open(presets_file, "r") as f:
                user_presets = json.load(f)
                presets.update(user_presets)
        except Exception as e:
            console.print(f"[bold red]Failed to load custom presets: {e}[/bold red]")
    return presets

def save_preset(name: str, features: list[str]) -> None:
    config_dir = Path.home() / ".config" / "spjaffolding"
    config_dir.mkdir(parents=True, exist_ok=True)
    presets_file = config_dir / "presets.json"
    
    presets = {}
    if presets_file.exists():
        try:
            with open(presets_file, "r") as f:
                presets = json.load(f)
        except Exception:
            pass
            
    presets[name] = features
    try:
        with open(presets_file, "w") as f:
            json.dump(presets, f, indent=4)
        console.print(f"[bold green]Saved preset '{name}' to {presets_file}.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Failed to save preset: {e}[/bold red]")

@app.command()
def main(
    tool_name: str = typer.Option(..., prompt="tool_name (e.g., bead, phaze)"),
    description: str = typer.Option(..., prompt="description"),
    preset: Optional[str] = typer.Option(
        None,
        help="A predefined preset. If omitted, opens the interactive multi-select menu.",
    ),
) -> None:
    """Entry point for scaffolding."""
    presets = load_presets()
    selected_features = []

    if preset:
        if preset not in presets:
            console.print(f"[bold red]Error: Preset '{preset}' not found. Available: {list(presets.keys())}[/bold red]")
            raise typer.Exit(code=1)
        selected_features = presets[preset]
        console.print(f"[bold blue]Using preset '{preset}': {selected_features}[/bold blue]")
    else:
        selected_features = questionary.checkbox(
            "Select the features to include in your project:",
            choices=AVAILABLE_FEATURES,
            style=CUSTOM_STYLE
        ).ask()
        
        if selected_features is None:
            console.print("[yellow]Scaffolding aborted by user.[/yellow]")
            raise typer.Exit(code=0)
            
        if selected_features:
            save_it = questionary.confirm(
                "Save this selection as a new preset?",
                default=False,
                style=CUSTOM_STYLE
            ).ask()
            if save_it:
                preset_name = questionary.text("Enter a name for the new preset:", style=CUSTOM_STYLE).ask()
                if preset_name:
                    save_preset(preset_name, selected_features)

    console.print(f"[bold green]Starting scaffolding for: {tool_name}[/bold green]")
    try:
        orchestrate_generation(
            tool_name=tool_name,
            description=description,
            features=selected_features
        )
        console.print(f"[bold blue]Successfully scaffolded {tool_name}![/bold blue]")
    except Exception as e:
        console.print(f"[bold red]Generation encountered an error: {e}[/bold red]")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
