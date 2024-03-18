import pytest
from prometheus_dirsize_exporter.exporter import BudgetedDirInfoWalker


@pytest.mark.parametrize("iops_budget,expected_sleep_calls", [(6, 0), (5, 1), (3, 1), (2, 2)])
def test_iops_budget_sleeping(iops_budget, expected_sleep_calls, mock_sleep, symlink_dir):
    """
    Verify that that going above the iops budget per second leads to time.sleep
    being called.
    """
    walker = BudgetedDirInfoWalker(iops_budget=iops_budget)

    walker.get_dir_info(symlink_dir)
    assert mock_sleep.calls == expected_sleep_calls


def test_symlink_size_and_entries(symlink_dir):
    """
    Verify that symlinks are not followed and counting the linked files size
    twice, but counted towards as entries.
    """
    walker = BudgetedDirInfoWalker()

    dir_info = walker.get_dir_info(symlink_dir)
    assert dir_info.entries_count == 3
    assert 100_000 < dir_info.size < 110_000


def test_limited_permissions(limited_permissions_dir):
    walker = BudgetedDirInfoWalker()

    dir_info = walker.get_dir_info(limited_permissions_dir)
