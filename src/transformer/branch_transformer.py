"""
Branch name transformer.
"""
from datetime import datetime
from typing import Optional


class BranchTransformer:
    """Transformer for branch names."""

    def __init__(self, add_date_suffix: bool = False) -> None:
        """
        Initialize branch transformer.

        Args:
            add_date_suffix: If True, append date suffix (yymmdd) to branch name
        """
        self.add_date_suffix = add_date_suffix

    def transform(self, branch_name: str) -> str:
        """
        Transform branch name.

        Args:
            branch_name: Original branch name

        Returns:
            Transformed branch name
        """
        if not branch_name:
            return branch_name

        if self.add_date_suffix:
            date_suffix = datetime.now().strftime("%y%m%d")
            return f"{branch_name}{date_suffix}"

        return branch_name

    def transform_revision(self, revision: Optional[str]) -> Optional[str]:
        """
        Transform revision (branch/tag name).

        Args:
            revision: Original revision string

        Returns:
            Transformed revision string, or None if revision is None
        """
        if not revision:
            return revision

        return self.transform(revision)
