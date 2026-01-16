"""
Revision filter for manifest projects.
"""
import re
from typing import List

from .models import Project


def is_hash_revision(revision: str) -> bool:
    """
    Check if revision is a hash (commit hash).

    Args:
        revision: Revision string to check

    Returns:
        True if revision is a hash, False otherwise
    """
    if not revision:
        return False

    # Hash patterns:
    # - 40 character hex string (full SHA-1)
    # - 7+ character hex string (short hash)
    # - Must be all hexadecimal characters
    hash_pattern = re.compile(r"^[0-9a-f]{7,40}$", re.IGNORECASE)

    return bool(hash_pattern.match(revision.strip()))


def filter_projects_by_revision(projects: List[Project]) -> List[Project]:
    """
    Filter projects to include only those with branch/tag revisions (exclude hash).

    Args:
        projects: List of projects to filter

    Returns:
        Filtered list of projects with non-hash revisions
    """
    filtered: List[Project] = []

    for project in projects:
        # Skip if no revision
        if not project.revision:
            continue

        # Skip if revision is a hash
        if is_hash_revision(project.revision):
            continue

        # Include projects with branch/tag names
        filtered.append(project)

    return filtered
