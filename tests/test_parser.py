"""
Tests for manifest parser.
"""
import tempfile
from pathlib import Path

import pytest

from src.manifest.parser import ManifestParser


@pytest.fixture
def sample_manifest_xml() -> str:
    """Sample manifest XML for testing."""
    return """<?xml version="1.0" encoding="UTF-8"?>
<manifest>
    <remote name="default" fetch="https://example.com/" />
    <default revision="main" remote="default" />
    
    <project name="platform/build" path="build" revision="main" />
    <project name="platform/frameworks/base" path="frameworks/base" revision="develop" />
    <project name="platform/system/core" path="system/core" revision="a1b2c3d" />
    <project name="platform/packages/apps/Settings" path="packages/apps/Settings" />
</manifest>
"""


@pytest.fixture
def manifest_file(sample_manifest_xml: str) -> Path:
    """Create a temporary manifest file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".xml", delete=False) as f:
        f.write(sample_manifest_xml)
        return Path(f.name)


class TestManifestParser:
    """Tests for ManifestParser."""

    def test_parse_manifest(self, manifest_file: Path) -> None:
        """Test parsing a valid manifest."""
        parser = ManifestParser(manifest_file)
        projects = parser.parse()

        assert len(projects) == 4
        assert projects[0].name == "platform/build"
        assert projects[0].path == "build"
        assert projects[0].revision == "main"

    def test_parse_nonexistent_file(self) -> None:
        """Test parsing non-existent file raises error."""
        with pytest.raises(FileNotFoundError):
            ManifestParser(Path("/nonexistent/file.xml"))

    def test_get_default_revision(self, manifest_file: Path) -> None:
        """Test getting default revision from manifest."""
        parser = ManifestParser(manifest_file)
        default_revision = parser.get_default_revision()
        assert default_revision == "main"
