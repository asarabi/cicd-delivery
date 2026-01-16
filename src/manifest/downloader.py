"""
Manifest downloader using repo init.
"""
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

from .models import ManifestConfig


class ManifestDownloader:
    """Downloader for repo manifests."""

    def __init__(self, config: ManifestConfig, work_dir: Optional[Path] = None) -> None:
        """
        Initialize downloader with manifest config.

        Args:
            config: Manifest configuration
            work_dir: Working directory for repo operations. If None, uses temp directory.
        """
        self.config = config
        self.work_dir = work_dir or Path(tempfile.mkdtemp(prefix="manifest_"))
        self.manifest_dir = self.work_dir / ".repo" / "manifests"

    def download(self) -> Path:
        """
        Download manifest using repo init.

        Returns:
            Path to the default.xml manifest file

        Raises:
            subprocess.CalledProcessError: If repo init fails
            FileNotFoundError: If default.xml is not found after download
        """
        # Create work directory
        self.work_dir.mkdir(parents=True, exist_ok=True)

        # Build repo init command
        cmd = ["repo", "init", "-u", self.config.repo_url, "--no-clone-bundle"]

        if self.config.branch:
            cmd.extend(["-b", self.config.branch])
        elif self.config.tag:
            cmd.extend(["-t", self.config.tag])

        # Run repo init
        try:
            result = subprocess.run(
                cmd,
                cwd=str(self.work_dir),
                capture_output=True,
                text=True,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            raise subprocess.CalledProcessError(
                e.returncode,
                e.cmd,
                f"repo init failed: {e.stderr}",
            ) from e
        except FileNotFoundError as e:
            raise FileNotFoundError(
                "repo command not found. Please install repo tool: "
                "https://source.android.com/setup/develop#installing-repo"
            ) from e

        # Find default.xml
        default_xml = self.manifest_dir / "default.xml"
        if not default_xml.exists():
            # Try to find any manifest file
            manifest_files = list(self.manifest_dir.glob("*.xml"))
            if manifest_files:
                default_xml = manifest_files[0]
            else:
                raise FileNotFoundError(
                    f"Manifest file not found in {self.manifest_dir}"
                )

        return default_xml

    def cleanup(self) -> None:
        """Clean up temporary files."""
        import shutil

        if self.work_dir.exists() and self.work_dir.is_dir():
            shutil.rmtree(self.work_dir)
