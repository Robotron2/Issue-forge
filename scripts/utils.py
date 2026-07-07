import json
import os
from pathlib import Path
import subprocess
from typing import Dict, Any
import yaml
from rich.console import Console

from models import RepoConfig

console = Console()

def load_config(root_dir: Path) -> RepoConfig:
    config_path = root_dir / "config.yml"
    
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
            if "owner" in data and "repo" in data:
                return RepoConfig(owner=data["owner"], repo=data["repo"])
    
    # Fallback to .env
    env_path = root_dir / ".env"
    if env_path.exists():
        from dotenv import load_dotenv
        load_dotenv(env_path)
    
    owner = os.getenv("OWNER") or os.getenv("GITHUB_OWNER")
    repo = os.getenv("REPO") or os.getenv("GITHUB_REPO")
    
    if not owner or not repo:
        console.print("[red]Error: Repository configuration not found. Please provide config.yml or .env with owner and repo.[/red]")
        exit(1)
        
    return RepoConfig(owner=owner, repo=repo)

def load_published_state(root_dir: Path) -> Dict[str, Any]:
    state_path = root_dir / "published.json"
    if not state_path.exists():
        return {}
    with open(state_path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_published_state(root_dir: Path, state: Dict[str, Any]) -> None:
    state_path = root_dir / "published.json"
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

def run_gh_command(cmd: list) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True)
