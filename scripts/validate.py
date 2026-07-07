import os
from pathlib import Path
import yaml
from rich.console import Console
from rich.table import Table

console = Console()
ROOT_DIR = Path(__file__).parent.parent
ISSUES_DIR = ROOT_DIR / "issues"

def main():
    if not ISSUES_DIR.exists():
        console.print("[red]issues/ directory does not exist. Run migrate.py first.[/red]")
        return
        
    yaml_files = list(ISSUES_DIR.glob("*.yml"))
    if not yaml_files:
        console.print("[yellow]No YAML files found to validate.[/yellow]")
        return
        
    all_ids = set()
    all_branches = set()
    errors = []
    
    issues_data = {}
    
    # First pass: collect all data
    for yf in yaml_files:
        with open(yf, "r", encoding="utf-8") as f:
            try:
                data = yaml.safe_load(f)
                if not isinstance(data, dict):
                    errors.append(f"{yf.name}: Invalid YAML structure (expected dict)")
                    continue
                issues_data[yf.name] = data
            except Exception as e:
                errors.append(f"{yf.name}: Failed to parse YAML: {e}")

    # Collect valid IDs for reference checking
    valid_ids = {data.get("id") for data in issues_data.values() if isinstance(data.get("id"), int)}

    # Second pass: validate
    for name, data in issues_data.items():
        # Required fields
        required = ["id", "type", "title", "description"]
        for req in required:
            if not data.get(req):
                errors.append(f"{name}: Missing required field '{req}'")
                
        # Commit message check
        if not data.get("commit"):
            errors.append(f"{name}: Missing commit message")
            
        # ID Uniqueness
        issue_id = data.get("id")
        if issue_id:
            if issue_id in all_ids:
                errors.append(f"{name}: Duplicate ID '{issue_id}'")
            all_ids.add(issue_id)
            
        # Branch uniqueness
        branch = data.get("branch")
        if branch:
            if branch in all_branches:
                errors.append(f"{name}: Duplicate branch '{branch}'")
            all_branches.add(branch)
            
        # References validation
        refs = data.get("references", [])
        if isinstance(refs, list):
            import re
            for ref in refs:
                found_ids = re.findall(r"#(\d+)", str(ref))
                for ref_id_str in found_ids:
                    ref_id = int(ref_id_str)
                    if ref_id not in valid_ids:
                        console.print(f"[yellow]Warning in {name}: Reference to issue {ref_id} which is not found locally.[/yellow]")

    if errors:
        console.print("[red]Validation Failed:[/red]")
        for err in errors:
            console.print(f"  - {err}")
        exit(1)
    else:
        console.print("[green]All YAML files passed validation![/green]")

if __name__ == "__main__":
    main()
