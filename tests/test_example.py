"""
Example test file to demonstrate test structure.
"""
import pytest


def test_example():
    """Example test case."""
    assert True


class TestExample:
    """Example test class."""

    def test_example_method(self):
        """Example test method."""
        assert 1 + 1 == 2

    @pytest.mark.unit
    def test_unit_example(self):
        """Example unit test with marker."""
        assert isinstance("test", str)
