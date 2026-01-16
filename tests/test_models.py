"""
Tests for data models.
"""
import pytest

from src.manifest.models import DeliveryConfig, ManifestConfig, Project


class TestProject:
    """Tests for Project model."""

    def test_project_creation(self) -> None:
        """Test creating a valid project."""
        project = Project(name="test/repo", path="test/repo", revision="main")
        assert project.name == "test/repo"
        assert project.path == "test/repo"
        assert project.revision == "main"

    def test_project_empty_name(self) -> None:
        """Test project with empty name raises error."""
        with pytest.raises(ValueError, match="name cannot be empty"):
            Project(name="", path="test")

    def test_project_empty_path(self) -> None:
        """Test project with empty path raises error."""
        with pytest.raises(ValueError, match="path cannot be empty"):
            Project(name="test", path="")


class TestManifestConfig:
    """Tests for ManifestConfig model."""

    def test_manifest_config_creation(self) -> None:
        """Test creating a valid manifest config."""
        config = ManifestConfig(repo_url="https://example.com/manifest", branch="main")
        assert config.repo_url == "https://example.com/manifest"
        assert config.branch == "main"
        assert config.tag is None

    def test_manifest_config_both_branch_and_tag(self) -> None:
        """Test that specifying both branch and tag raises error."""
        with pytest.raises(ValueError, match="Cannot specify both branch and tag"):
            ManifestConfig(
                repo_url="https://example.com/manifest", branch="main", tag="v1.0"
            )

    def test_manifest_config_empty_url(self) -> None:
        """Test manifest config with empty URL raises error."""
        with pytest.raises(ValueError, match="repository URL cannot be empty"):
            ManifestConfig(repo_url="")


class TestDeliveryConfig:
    """Tests for DeliveryConfig model."""

    def test_delivery_config_ssh(self) -> None:
        """Test creating SSH delivery config."""
        config = DeliveryConfig(
            gerrit_url="ssh://gerrit.example.com",
            auth_method="ssh",
            ssh_key_path="/path/to/key",
        )
        assert config.auth_method == "ssh"
        assert config.ssh_key_path == "/path/to/key"

    def test_delivery_config_http(self) -> None:
        """Test creating HTTP delivery config."""
        config = DeliveryConfig(
            gerrit_url="https://gerrit.example.com",
            auth_method="http",
            username="user",
            password="pass",
        )
        assert config.auth_method == "http"
        assert config.username == "user"

    def test_delivery_config_invalid_auth_method(self) -> None:
        """Test invalid auth method raises error."""
        with pytest.raises(ValueError, match="auth_method must be"):
            DeliveryConfig(gerrit_url="https://example.com", auth_method="invalid")

    def test_delivery_config_ssh_without_key(self) -> None:
        """Test SSH config without key raises error."""
        with pytest.raises(ValueError, match="ssh_key_path is required"):
            DeliveryConfig(gerrit_url="ssh://example.com", auth_method="ssh")

    def test_delivery_config_http_without_username(self) -> None:
        """Test HTTP config without username raises error."""
        with pytest.raises(ValueError, match="username is required"):
            DeliveryConfig(gerrit_url="https://example.com", auth_method="http")
