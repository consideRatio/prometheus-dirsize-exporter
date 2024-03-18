import os
import shutil
import tempfile
import time
from pathlib import Path

import pytest

def create_file(name, kb=100):
    with open(name, "wb") as f:
        f.truncate(kb * 1000)

class MockCheckCall:
    def __init__(self):
        self.commands = []

    def __call__(self, cmd, **kwargs):
        self.commands.append((cmd, kwargs))
    
    @property
    def calls(self):
        return len(self.commands)
    

@pytest.fixture
def mock_sleep(monkeypatch):
    """
    This fixture mocks time.sleep,
    """
    mock_sleep = MockCheckCall()
    monkeypatch.setattr(time, "sleep", mock_sleep)

    yield mock_sleep


@pytest.fixture
def temp_cwd(monkeypatch):
    with tempfile.TemporaryDirectory() as temp_dir:
        monkeypatch.chdir(temp_dir)
        yield temp_dir


@pytest.fixture
def symlink_dir(temp_cwd):
    create_file("file", kb=100)
    os.symlink("file", "file_symlink")
    yield temp_cwd


@pytest.fixture
def limited_permissions_dir(temp_cwd, monkeypatch):
    if os.getuid() != 0:
        pytest.skip("Needs to be run as root user")

    create_file("file", kb=100)
    yield temp_cwd
