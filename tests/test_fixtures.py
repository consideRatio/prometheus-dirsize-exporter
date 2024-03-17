import os
from glob import glob

def test_fixture(test_parent_dir):
    assert test_parent_dir == os.getcwd()
    assert sorted(glob("*")) == ["test_recursion", "test_symlink"]
