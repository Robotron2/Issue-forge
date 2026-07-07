import os
from pathlib import Path
import yaml
from jinja2 import Environment, FileSystemLoader
from rich.progress import Progress
from rich.console import Console

console = Console()

ROOT_DIR = Path(__file__).parent.parent
ISSUES_DIR = ROOT_DIR / "issues"
GENERATED_DIR = ROOT_DIR / "generated"
TEMPLATES_DIR = ROOT_DIR / "templates"

def main():
    if not ISSUES_DIR.exists() or not list(ISSUES_DIR.glob("*.yml")):
        console.print("[red]No YAML issues found in issues/ directory.[/red]")
        return
        
    GENERATED_DIR.mkdir(exist_ok=True)
    
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR), trim_blocks=True, lstrip_blocks=True)
    try:
        template = env.get_template("issue.md.j2")
    except Exception as e:
        console.print(f"[red]Failed to load Jinja2 template: {e}[/red]")
        return
        
    yaml_files = list(ISSUES_DIR.glob("*.yml"))
    
    with Progress() as progress:
        task = progress.add_task("[cyan]Generating Markdown...", total=len(yaml_files))
        
        for yf in yaml_files:
            try:
                with open(yf, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    
                rendered = template.render(**data)
                
                # Make sure rendered markdown ends with a single newline
                rendered = rendered.strip() + "\n"
                
                out_path = GENERATED_DIR / f"{data['id']:03d}.md"
                with open(out_path, "w", encoding="utf-8") as out:
                    out.write(rendered)
            except Exception as e:
                console.print(f"[red]Error generating markdown for {yf.name}: {e}[/red]")
            finally:
                progress.advance(task)
                
    console.print(f"[green]Generated {len(yaml_files)} issues.[/green]")

if __name__ == "__main__":
    main()
