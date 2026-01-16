"""
Manifest XML parser.
"""
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Optional

from .models import Project


class ManifestParser:
    """Parser for repo manifest XML files."""

    def __init__(self, manifest_path: Path) -> None:
        """
        Initialize parser with manifest file path.

        Args:
            manifest_path: Path to the manifest XML file
        """
        self.manifest_path = manifest_path
        if not manifest_path.exists():
            raise FileNotFoundError(f"Manifest file not found: {manifest_path}")

    def parse(self) -> List[Project]:
        """
        Parse manifest XML and extract projects.

        Returns:
            List of Project objects

        Raises:
            ET.ParseError: If XML parsing fails
        """
        try:
            tree = ET.parse(self.manifest_path)
            root = tree.getroot()
        except ET.ParseError as e:
            raise ET.ParseError(f"Failed to parse manifest XML: {e}") from e

        projects: List[Project] = []
        default_remote = root.get("remote", "default")

        # Parse default remote if exists
        for remote_elem in root.findall("remote"):
            if remote_elem.get("name") == default_remote:
                default_remote_url = remote_elem.get("fetch", "")
                break
        else:
            default_remote_url = ""

        # Parse projects
        for project_elem in root.findall("project"):
            name = project_elem.get("name", "")
            path = project_elem.get("path", name)
            revision = project_elem.get("revision")
            remote = project_elem.get("remote", default_remote)

            # Get remote URL if specified
            remote_url = default_remote_url
            for remote_elem in root.findall("remote"):
                if remote_elem.get("name") == remote:
                    remote_url = remote_elem.get("fetch", "")
                    break

            if name:
                project = Project(
                    name=name,
                    path=path,
                    revision=revision,
                    remote=remote_url if remote_url else None,
                )
                projects.append(project)

        # Handle default revision from manifest
        default_elem = root.find("default")
        default_revision = None
        if default_elem is not None:
            default_revision = default_elem.get("revision")

        # Apply default revision to projects without revision
        if default_revision:
            for project in projects:
                if not project.revision:
                    project.revision = default_revision

        return projects

    def get_default_revision(self) -> Optional[str]:
        """
        Get default revision from manifest.

        Returns:
            Default revision string or None
        """
        try:
            tree = ET.parse(self.manifest_path)
            root = tree.getroot()
            default_elem = root.find("default")
            if default_elem is not None:
                return default_elem.get("revision")
        except (ET.ParseError, FileNotFoundError):
            pass
        return None
