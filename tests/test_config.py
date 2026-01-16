"""
Tests for configuration loader.
"""
import os
import tempfile
from pathlib import Path

import pytest
import yaml

from src.config.settings import ConfigLoader


@pytest.fixture
def sample_config() -> dict:
    """Sample configuration data."""
    return {
        "manifest": {
            "repo_url": "https://example.com/manifest",
            "branch": "main",
        },
        "delivery": {
            "gerrit_url": "https://gerrit.example.com",
            "auth": {
                "method": "ssh",
                "ssh_key_path": "~/.ssh/id_rsa",
            },
            "branch_transform": False,
            "repo_alias": None,
        },
    }


@pytest.fixture
def config_file(sample_config: dict) -> Path:
    """Create a temporary config file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(sample_config, f)
        return Path(f.name)


class TestConfigLoader:
    """Tests for ConfigLoader."""

    def test_load_config(self, config_file: Path) -> None:
        """Test loading valid configuration."""
        loader = ConfigLoader(config_file)
        manifest_config, delivery_config = loader.load()

        assert manifest_config.repo_url == "https://example.com/manifest"
        assert manifest_config.branch == "main"
        assert delivery_config.gerrit_url == "https://gerrit.example.com"
        assert delivery_config.auth_method == "ssh"

    def test_load_nonexistent_file(self) -> None:
        """Test loading non-existent file raises error."""
        with pytest.raises(FileNotFoundError):
            ConfigLoader(Path("/nonexistent/config.yaml"))

    def test_load_with_env_vars(self, sample_config: dict) -> None:
        """Test loading config with environment variables."""
        # Remove username/password from config
        sample_config["delivery"]["auth"]["method"] = "http"
        del sample_config["delivery"]["auth"]["ssh_key_path"]

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(sample_config, f)
            config_path = Path(f.name)

        try:
            # Set environment variables
            os.environ["GERRIT_USERNAME"] = "testuser"
            os.environ["GERRIT_PASSWORD"] = "testpass"

            loader = ConfigLoader(config_path)
            _, delivery_config = loader.load()

            assert delivery_config.username == "testuser"
            assert delivery_config.password == "testpass"
        finally:
            # Cleanup
            os.environ.pop("GERRIT_USERNAME", None)
            os.environ.pop("GERRIT_PASSWORD", None)
            config_path.unlink()
