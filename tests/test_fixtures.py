import os
from glob import glob

def test_symlink_dir(symlink_dir):
    assert symlink_dir == os.getcwd()
    assert sorted(glob("*")) == ["file", "file_symlink"]
