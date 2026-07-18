import os
import re
import yaml
from pathlib import Path
from rich.progress import Progress
from utils import console

ROOT_DIR = Path(__file__).parent.parent
ORIGINAL_DIR = ROOT_DIR / "original"
ISSUES_DIR = ROOT_DIR / "issues"

ISSUE_HEADER_RE = re.compile(r"^# Issue #?(\d+)\s*—\s*(?:([a-zA-Z]+):\s*)?(.*)$")

TYPE_TO_LABEL = {
    "feat": "enhancement",
    "fix": "bug",
    "docs": "documentation",
    "refactor": "refactor",
    "chore": "maintenance"
}

def parse_list_or_paragraphs(text: str) -> list[str]:
    if not text:
        return []
    lines = [line.strip() for line in text.split("\n")]
    items = []
    current_item = []
    
    is_list = any(line.startswith("* ") or line.startswith("- ") for line in lines)
    
    if is_list:
        for line in lines:
            if line.startswith("* ") or line.startswith("- "):
                if current_item:
                    items.append("\n".join(current_item).strip())
                # Remove checkbox if present
                content = re.sub(r"^[*|-]\s+(\[\s*\]\s*)?", "", line)
                current_item = [content]
            elif line and current_item:
                current_item.append(line)
        if current_item:
            items.append("\n".join(current_item).strip())
    else:
        # paragraphs
        for block in text.split("\n\n"):
            block = block.strip()
            if block:
                items.append(block)
                
    return items

def parse_issue(content: str) -> dict:
    lines = content.split('\n')
    
    header_match = None
    for line in lines:
        if ISSUE_HEADER_RE.match(line):
            header_match = ISSUE_HEADER_RE.match(line)
            break
            
    if not header_match:
        raise ValueError("Could not find issue header matching '# Issue #<id> — <type>: <title>' or '# Issue <id> — <title>'")
        
    issue_id = int(header_match.group(1))
    issue_type = header_match.group(2) or "feat" # Default to feat if no type provided
    title = header_match.group(3).strip()
    
    # Split by sections
    sections = {}
    current_section = None
    current_content = []
    
    for line in lines:
        if line.startswith("## "):
            if current_section:
                sections[current_section] = "\n".join(current_content).strip()
            # normalize section names
            current_section = line[3:].strip().lower()
            current_content = []
        elif current_section and line != "---":
            current_content.append(line)
            
    if current_section:
        sections[current_section] = "\n".join(current_content).strip()
        
    # Required sections check (flexible for 'and' vs '&')
    if "description" not in sections:
        raise ValueError(f"Issue {issue_id} is missing required section: 'description'")
        
    req_context = sections.get("requirements & context") or sections.get("requirements and context")
    if req_context is None:
        raise ValueError(f"Issue {issue_id} is missing required section: 'requirements and context'")
        
    # Extract specific fields
    description = sections.get("description", "")
    requirements = parse_list_or_paragraphs(req_context)
    acceptance = parse_list_or_paragraphs(sections.get("acceptance criteria", ""))
    out_of_scope = parse_list_or_paragraphs(sections.get("out of scope", ""))
    references = parse_list_or_paragraphs(sections.get("references", ""))
    testing = sections.get("testing notes", "").strip()
    
    # Suggested Execution (Branch)
    branch = None
    exec_text = sections.get("suggested execution", "")
    branch_match = re.search(r"git checkout -b\s+([^\s]+)", exec_text)
    if branch_match:
        branch = branch_match.group(1)
        
    # Suggested Commit (or Example Commit)
    commit = None
    commit_text = sections.get("suggested commit message") or sections.get("example commit message") or ""
    # extract code block (handling weird attributes like ```text id="xxx")
    code_block_match = re.search(r"```.*?\n(.*?)```", commit_text, re.DOTALL)
    if code_block_match:
        commit = code_block_match.group(1).strip()
    else:
        # fallback to just the text if no codeblock
        if commit_text:
            commit = commit_text.strip()
            
    labels = []
    if issue_type in TYPE_TO_LABEL:
        labels.append(TYPE_TO_LABEL[issue_type])
        
    return {
        "id": issue_id,
        "type": issue_type,
        "title": title,
        "branch": branch,
        "commit": commit,
        "description": description,
        "requirements": requirements,
        "acceptance": acceptance,
        "out_of_scope": out_of_scope,
        "testing": testing,
        "references": references,
        "labels": labels
    }

GENERATED_DIR = ROOT_DIR / "generated"

def main():
    if not ORIGINAL_DIR.exists():
        console.print("[red]original/ directory does not exist.[/red]")
        return
        
    ISSUES_DIR.mkdir(exist_ok=True)
    
    # Auto-cleanup previous run's YAML files
    old_yamls = list(ISSUES_DIR.glob("*.yml"))
    if old_yamls:
        console.print(f"[yellow]Cleaning up {len(old_yamls)} old issues from previous runs...[/yellow]")
        for f in old_yamls:
            f.unlink()
            
    # Auto-cleanup previous run's generated Markdown files
    if GENERATED_DIR.exists():
        old_mds = list(GENERATED_DIR.glob("*.md"))
        for f in old_mds:
            f.unlink()
    
    md_files = list(ORIGINAL_DIR.glob("*.md"))
    if not md_files:
        console.print("[yellow]No markdown files found in original/.[/yellow]")
        return
        
    # First, gather all issue blocks across all files
    issue_blocks = []
    
    for md_file in md_files:
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Split issues by looking for "\n# Issue"
        parts = re.split(r"(?m)^# Issue\b", content)
        for part in parts:
            part = part.strip()
            if not part:
                continue
            # restore the '# Issue ' prefix
            if part.startswith("#"):
                # Handle `#1 — ...`
                part = "# Issue " + part
            else:
                part = "# Issue " + part
            issue_blocks.append((md_file.name, part))
            
    if not issue_blocks:
        console.print("[yellow]No valid issues found in markdown files.[/yellow]")
        return
        
    success_count = 0
    with Progress() as progress:
        task = progress.add_task("[cyan]Migrating issues...", total=len(issue_blocks))
        
        for file_name, block in issue_blocks:
            try:
                parsed = parse_issue(block)
                issue_id = parsed["id"]
                
                # Cleanup empty strings from testing if empty
                if not parsed.get("testing"):
                    parsed["testing"] = None
                    
                # Format to a nice YAML
                yaml_path = ISSUES_DIR / f"{issue_id:03d}.yml"
                
                # Remove None values to keep YAML clean
                clean_parsed = {k: v for k, v in parsed.items() if v is not None and v != "" and v != []}
                # However, the user expected explicit empty lists or fields if possible? Let's just dump clean_parsed.
                # Actually, I'll dump exactly the keys as in models to keep it consistent, but it's fine.
                
                with open(yaml_path, "w", encoding="utf-8") as yf:
                    yaml.dump(clean_parsed, yf, sort_keys=False, default_flow_style=False, allow_unicode=True)
                    
                success_count += 1
            except Exception as e:
                console.print(f"[red]Error parsing issue in {file_name}: {e}[/red]")
            finally:
                progress.advance(task)
                
    console.print(f"[green]Successfully migrated {success_count} issues to {ISSUES_DIR}.[/green]")

if __name__ == "__main__":
    main()
