from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Issue:
    id: int
    type: str
    title: str
    description: str
    branch: Optional[str] = None
    commit: Optional[str] = None
    requirements: List[str] = field(default_factory=list)
    acceptance: List[str] = field(default_factory=list)
    out_of_scope: List[str] = field(default_factory=list)
    testing: Optional[str] = None
    references: List[str] = field(default_factory=list)
    labels: List[str] = field(default_factory=list)

@dataclass
class RepoConfig:
    owner: str
    repo: str
