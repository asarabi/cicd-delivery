"""
Configuration management.
"""
import os
from pathlib import Path
from typing import Optional

import yaml

from lib.manifest.models import DeliveryConfig, ManifestConfig


class ConfigLoader:
    """Loader for configuration files."""

    def __init__(self, config_path: Path) -> None:
        """
        Initialize config loader.

        Args:
            config_path: Path to configuration file (YAML)
        """
        self.config_path = config_path
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

    def load(self) -> tuple[ManifestConfig, DeliveryConfig]:
        """
        Load configuration from file.

        Returns:
            Tuple of (ManifestConfig, DeliveryConfig)

        Raises:
            yaml.YAMLError: If YAML parsing fails
            ValueError: If required fields are missing
        """
        with open(self.config_path, "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f)

        if not config_data:
            raise ValueError("Configuration file is empty")

        # Load manifest config
        manifest_data = config_data.get("manifest", {})
        manifest_config = ManifestConfig(
            repo_url=manifest_data.get("repo_url", ""),
            branch=manifest_data.get("branch"),
            tag=manifest_data.get("tag"),
            default_revision=manifest_data.get("default_revision"),
        )

        # Load delivery config
        delivery_data = config_data.get("delivery", {})
        auth_data = delivery_data.get("auth", {})

        # Resolve paths relative to config file
        ssh_key_path = auth_data.get("ssh_key_path")
        if ssh_key_path and not Path(ssh_key_path).is_absolute():
            ssh_key_path = str(self.config_path.parent / ssh_key_path)

        # Get credentials from environment if not in config
        username = auth_data.get("username") or os.getenv("GERRIT_USERNAME")
        password = auth_data.get("password") or os.getenv("GERRIT_PASSWORD")

        delivery_config = DeliveryConfig(
            gerrit_url=delivery_data.get("gerrit_url", ""),
            auth_method=auth_data.get("method", "ssh"),
            ssh_key_path=ssh_key_path,
            username=username,
            password=password,
            branch_transform=delivery_data.get("branch_transform", False),
            repo_alias=delivery_data.get("repo_alias"),
        )

        return manifest_config, delivery_config
