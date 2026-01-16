"""
Repository name transformer.
"""
from typing import Optional


class RepoTransformer:
    """Transformer for repository names/paths."""

    def __init__(self, alias: Optional[str] = None) -> None:
        """
        Initialize repository transformer.

        Args:
            alias: Alias to insert in the middle of repository path
        """
        self.alias = alias

    def transform(self, repo_name: str) -> str:
        """
        Transform repository name by inserting alias in the middle.

        Args:
            repo_name: Original repository name/path

        Returns:
            Transformed repository name with alias inserted
        """
        if not repo_name or not self.alias:
            return repo_name

        # Split path by '/'
        parts = repo_name.split("/")

        if len(parts) <= 1:
            # If no path separator, prepend alias
            return f"{self.alias}/{repo_name}"

        # Insert alias after first part
        # e.g., "platform/build" -> "platform/alias/build"
        transformed_parts = [parts[0], self.alias] + parts[1:]
        return "/".join(transformed_parts)
