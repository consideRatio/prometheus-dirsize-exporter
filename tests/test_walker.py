import pytest
from timeit import timeit
from prometheus_dirsize_exporter.exporter import BudgetedDirInfoWalker


@pytest.mark.parametrize("iops_budget,min_time,max_time", [(10, 0.5, 1.5), (1000, 0, 0.5)])
def test_budget(test_parent_dir, iops_budget, min_time, max_time):
    walker = BudgetedDirInfoWalker(iops_budget=iops_budget)

    def walk():
        for subdir_info in walker.get_subdirs_info(test_parent_dir):
            print(subdir_info)

    duration_s = timeit(walk, number=1)
    assert duration_s > min_time
    assert duration_s < max_time
