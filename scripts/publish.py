import argparse
import os
import subprocess
from pathlib import Path
import yaml
from jinja2 import Environment, FileSystemLoader
from rich.console import Console
from rich.prompt import Confirm

from utils import load_config, load_published_state, save_published_state

console = Console()

ROOT_DIR = Path(__file__).parent.parent
ISSUES_DIR = ROOT_DIR / "issues"
TEMPLATES_DIR = ROOT_DIR / "templates"
GENERATED_DIR = ROOT_DIR / "generated"

def parse_args():
    parser = argparse.ArgumentParser(description="Publish issues to GitHub")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen without publishing")
    parser.add_argument("--issue", type=int, help="Publish only a specific issue ID")
    parser.add_argument("--range", type=str, help="Publish issues in a range (e.g. 7-12)")
    parser.add_argument("--yes", "-y", action="store_true", help="Skip confirmation prompt")
    return parser.parse_args()

def main():
    args = parse_args()
    config = load_config(ROOT_DIR)
    
    if not ISSUES_DIR.exists():
        console.print("[red]No issues/ directory found. Please migrate first.[/red]")
        return
        
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR), trim_blocks=True, lstrip_blocks=True)
    try:
        template = env.get_template("issue.md.j2")
    except Exception as e:
        console.print(f"[red]Failed to load Jinja2 template: {e}[/red]")
        return
        
    published_state = load_published_state(ROOT_DIR)
    
    yaml_files = sorted(list(ISSUES_DIR.glob("*.yml")))
    
    to_publish = []
    already_published_count = 0
    skipped_interactive_count = 0
    published_count = 0
    
    # Filter targets based on args
    target_ids = set()
    if args.issue:
        target_ids.add(args.issue)
    elif args.range:
        try:
            start, end = map(int, args.range.split("-"))
            target_ids.update(range(start, end + 1))
        except ValueError:
            console.print("[red]Invalid range format. Use START-END (e.g., 7-12)[/red]")
            return
            
    for yf in yaml_files:
        try:
            with open(yf, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                
            issue_id = data["id"]
            
            # If target ids specified, skip if not in target
            if target_ids and issue_id not in target_ids:
                continue
                
            # Check if already published
            # Ensure key is zero-padded string as specified by user example
            state_key = f"{issue_id:03d}"
            if state_key in published_state:
                console.print(f"[yellow]Skipping #{issue_id}: already published as GitHub Issue #{published_state[state_key].get('github_issue')}[/yellow]")
                already_published_count += 1
                continue
                
            to_publish.append(data)
            
        except Exception as e:
            console.print(f"[red]Failed to read {yf.name}: {e}[/red]")
            
    if not to_publish:
        console.print("[green]No new issues to publish.[/green]")
        if already_published_count > 0:
            console.print(f"[dim]{already_published_count} issues were skipped because they are already published.[/dim]")
        return
        
    try:
        for data in to_publish:
            issue_id = data["id"]
            title = data["title"]
            labels = data.get("labels", [])
            state_key = f"{issue_id:03d}"
            
            console.print(f"\n[cyan]Target Repository:[/cyan] {config.owner}/{config.repo}")
            console.print(f"[cyan]Local Issue ID:[/cyan] {issue_id}")
            console.print(f"[cyan]Title:[/cyan] {title}")
            
            if not args.yes and not args.dry_run:
                if not Confirm.ask("Publish this issue?"):
                    console.print("[yellow]Skipping...[/yellow]")
                    skipped_interactive_count += 1
                    continue
                    
            # Render markdown body
            body = template.render(**data)
            body = body.strip() + "\n"
            
            # We also write it to generated folder as per user requirement: 
            # "It should still write the Markdown to generated/ for your review, but it shouldn't read it back to publish."
            GENERATED_DIR.mkdir(exist_ok=True)
            with open(GENERATED_DIR / f"{state_key}.md", "w", encoding="utf-8") as gen_f:
                gen_f.write(body)
                
            cmd = [
                "gh", "issue", "create",
                "--repo", f"{config.owner}/{config.repo}",
                "--title", title,
                "--body-file", "-"
            ]
            for label in labels:
                cmd.extend(["--label", label])
                
            if args.dry_run:
                console.print(f"[magenta]DRY RUN: Would execute[/magenta] {' '.join(cmd)}")
                continue
                
            console.print("[cyan]Publishing...[/cyan]")
            
            # Run gh command with body as stdin
            try:
                result = subprocess.run(cmd, input=body, capture_output=True, text=True, check=True)
                # Output from `gh issue create` is usually the URL: https://github.com/org/repo/issues/123
                output_url = result.stdout.strip()
                github_issue_num = int(output_url.split("/")[-1])
                
                console.print(f"[green]Successfully published! GitHub Issue #{github_issue_num}[/green]")
                
                published_state[state_key] = {"github_issue": github_issue_num}
                save_published_state(ROOT_DIR, published_state)
                published_count += 1
                
            except subprocess.CalledProcessError as e:
                console.print(f"[red]Failed to publish issue #{issue_id}:[/red]")
                console.print(e.stderr)
                console.print("[red]Aborting further publishing.[/red]")
                break
                
    except KeyboardInterrupt:
        console.print("\n[yellow]Publishing interrupted by user (Ctrl+C).[/yellow]")
        
    finally:
        # Print summary
        console.print("\n[bold]Publishing Summary:[/bold]")
        console.print(f"  - [green]{published_count} newly published[/green]")
        console.print(f"  - [yellow]{already_published_count} skipped (already on GitHub)[/yellow]")
        console.print(f"  - [dim]{skipped_interactive_count} skipped interactively[/dim]")

if __name__ == "__main__":
    main()
