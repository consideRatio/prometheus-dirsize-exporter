import os
import shutil
import tempfile

import pytest


@pytest.fixture
def test_parent_dir(monkeypatch):
    """
    This fixture puts us in a temporary directory matching
    tests/test_parent_dir.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        cwd = os.getcwd()
        test_parent_dir = os.path.join(cwd, "tests/test_parent_dir")

        # populate and enter the directory
        shutil.copytree(test_parent_dir, temp_dir, dirs_exist_ok=True)
        monkeypatch.chdir(temp_dir)

        yield temp_dir
