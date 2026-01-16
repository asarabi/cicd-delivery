"""
Data models for manifest parsing.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Project:
    """Represents a project in the manifest."""

    name: str
    path: str
    revision: Optional[str] = None
    remote: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate project data."""
        if not self.name:
            raise ValueError("Project name cannot be empty")
        if not self.path:
            raise ValueError("Project path cannot be empty")


@dataclass
class ManifestConfig:
    """Configuration for manifest download."""

    repo_url: str
    branch: Optional[str] = None
    tag: Optional[str] = None
    default_revision: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate manifest config."""
        if not self.repo_url:
            raise ValueError("Manifest repository URL cannot be empty")
        if self.branch and self.tag:
            raise ValueError("Cannot specify both branch and tag")


@dataclass
class DeliveryConfig:
    """Configuration for delivery to Gerrit."""

    gerrit_url: str
    auth_method: str  # 'ssh' or 'http'
    ssh_key_path: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    branch_transform: bool = False  # 브랜치 이름에 날짜 추가
    repo_alias: Optional[str] = None  # 레포지토리 이름 중간에 추가할 alias

    def __post_init__(self) -> None:
        """Validate delivery config."""
        if not self.gerrit_url:
            raise ValueError("Gerrit URL cannot be empty")
        if self.auth_method not in ("ssh", "http"):
            raise ValueError("auth_method must be 'ssh' or 'http'")
        if self.auth_method == "ssh" and not self.ssh_key_path:
            raise ValueError("ssh_key_path is required for SSH authentication")
        if self.auth_method == "http" and not self.username:
            raise ValueError("username is required for HTTP authentication")
