"""
Tests for revision filter.
"""
from src.manifest.filter import filter_projects_by_revision, is_hash_revision
from src.manifest.models import Project


class TestIsHashRevision:
    """Tests for hash revision detection."""

    def test_full_sha1_hash(self) -> None:
        """Test full SHA-1 hash detection."""
        assert is_hash_revision("a1b2c3d4e5f6789012345678901234567890abcd")
        assert is_hash_revision("A1B2C3D4E5F6789012345678901234567890ABCD")

    def test_short_hash(self) -> None:
        """Test short hash detection."""
        assert is_hash_revision("a1b2c3d")
        assert is_hash_revision("1234567")

    def test_branch_name(self) -> None:
        """Test branch names are not hashes."""
        assert not is_hash_revision("main")
        assert not is_hash_revision("develop")
        assert not is_hash_revision("feature/new-feature")

    def test_tag_name(self) -> None:
        """Test tag names are not hashes."""
        assert not is_hash_revision("v1.0.0")
        assert not is_hash_revision("release-2024")

    def test_empty_string(self) -> None:
        """Test empty string is not a hash."""
        assert not is_hash_revision("")
        assert not is_hash_revision(None)  # type: ignore

    def test_invalid_hash_length(self) -> None:
        """Test strings that are too short are not hashes."""
        assert not is_hash_revision("abc")
        assert not is_hash_revision("123456")


class TestFilterProjectsByRevision:
    """Tests for project filtering."""

    def test_filter_hash_revisions(self) -> None:
        """Test filtering out hash revisions."""
        projects = [
            Project(name="repo1", path="repo1", revision="main"),
            Project(name="repo2", path="repo2", revision="a1b2c3d4e5f6"),
            Project(name="repo3", path="repo3", revision="develop"),
            Project(name="repo4", path="repo4", revision="1234567890abcdef"),
        ]

        filtered = filter_projects_by_revision(projects)
        assert len(filtered) == 2
        assert filtered[0].name == "repo1"
        assert filtered[1].name == "repo3"

    def test_filter_no_revision(self) -> None:
        """Test filtering out projects without revision."""
        projects = [
            Project(name="repo1", path="repo1", revision="main"),
            Project(name="repo2", path="repo2", revision=None),
            Project(name="repo3", path="repo3", revision="develop"),
        ]

        filtered = filter_projects_by_revision(projects)
        assert len(filtered) == 2
        assert filtered[0].name == "repo1"
        assert filtered[1].name == "repo3"

    def test_filter_all_hash(self) -> None:
        """Test filtering when all projects have hash revisions."""
        projects = [
            Project(name="repo1", path="repo1", revision="a1b2c3d"),
            Project(name="repo2", path="repo2", revision="1234567"),
        ]

        filtered = filter_projects_by_revision(projects)
        assert len(filtered) == 0

    def test_filter_empty_list(self) -> None:
        """Test filtering empty list."""
        filtered = filter_projects_by_revision([])
        assert len(filtered) == 0
