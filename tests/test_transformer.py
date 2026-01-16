"""
Tests for transformers.
"""
from lib.transformer.branch_transformer import BranchTransformer
from lib.transformer.repo_transformer import RepoTransformer


class TestBranchTransformer:
    """Tests for BranchTransformer."""

    def test_transform_without_date(self) -> None:
        """Test branch transformation without date suffix."""
        transformer = BranchTransformer(add_date_suffix=False)
        assert transformer.transform("main") == "main"
        assert transformer.transform("develop") == "develop"

    def test_transform_with_date(self) -> None:
        """Test branch transformation with date suffix."""
        transformer = BranchTransformer(add_date_suffix=True)
        result = transformer.transform("main")
        # Should be main + 6 digit date (yymmdd)
        assert result.startswith("main")
        assert len(result) == len("main") + 6
        assert result[4:].isdigit()

    def test_transform_revision(self) -> None:
        """Test revision transformation."""
        transformer = BranchTransformer(add_date_suffix=False)
        assert transformer.transform_revision("main") == "main"
        assert transformer.transform_revision(None) is None

    def test_transform_empty_string(self) -> None:
        """Test transforming empty string."""
        transformer = BranchTransformer(add_date_suffix=False)
        assert transformer.transform("") == ""


class TestRepoTransformer:
    """Tests for RepoTransformer."""

    def test_transform_without_alias(self) -> None:
        """Test repository transformation without alias."""
        transformer = RepoTransformer(alias=None)
        assert transformer.transform("platform/build") == "platform/build"
        assert transformer.transform("test/repo") == "test/repo"

    def test_transform_with_alias(self) -> None:
        """Test repository transformation with alias."""
        transformer = RepoTransformer(alias="alias")
        assert transformer.transform("platform/build") == "platform/alias/build"
        assert transformer.transform("test/repo") == "test/alias/repo"

    def test_transform_single_part(self) -> None:
        """Test transforming repository with single part."""
        transformer = RepoTransformer(alias="alias")
        assert transformer.transform("repo") == "alias/repo"

    def test_transform_empty_string(self) -> None:
        """Test transforming empty string."""
        transformer = RepoTransformer(alias="alias")
        assert transformer.transform("") == ""
