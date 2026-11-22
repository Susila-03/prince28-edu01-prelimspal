from pathlib import Path


def test_api_test_suite_exists():
    """Check that the API test suite is present in the unit tests folder."""
    api_test_file = Path(__file__).parent / "unit" / "test_api.py"

    assert api_test_file.is_file()
