import sys
from pathlib import Path

import numpy as np
import pytest
from icecream import ic

# --> Puzzle solution


def read_points(input_data):
    data = np.array(
        [[int(i) for i in row.split(",")] for row in input_data.splitlines()]
    )
    ic(data)
    return data


def combine_groups(indexes, groups):
    i1, i2 = indexes
    s1 = groups.pop(i1)
    s2 = groups.pop(i2)
    s3 = s1.union(s2)

    for i in s3:
        groups[i] = s3

    ic(indexes, groups)


def solve(input_data):
    distances = {}

    points = read_points(input_data)
    n_points = points.shape[0]

    groups = {i: {i} for i in range(n_points)}
    ic(groups)

    for i in range(n_points):
        for j in range(i + 1, n_points):
            distances[i, j] = np.linalg.norm(points[i] - points[j])

    lengths = sorted(zip(distances.values(), distances.keys()))

    for _, keys in lengths:
        i1, i2 = keys
        if i1 not in groups[i2]:
            combine_groups(keys, groups)
        if len(groups[0]) == n_points:
            return points[i1][0] * points[i2][0]

    raise Exception("oops")


# --> Test driven development helpers


# Test any examples given in the problem

sample_input = Path("input-sample.txt").read_text().strip()
EXAMPLES = [
    (sample_input, 25272),
]


@pytest.mark.parametrize("sample_data,sample_solution", EXAMPLES, ids=("sample",))
def test_samples(sample_data, sample_solution) -> None:
    assert solve(sample_data) == sample_solution


# --> Setup and run

if __name__ == "__main__":
    #  Run the test examples with icecream debug-trace turned on
    ic.enable()
    ex = pytest.main([__file__, "--capture=tee-sys", "-v"])
    if ex not in {pytest.ExitCode.OK, pytest.ExitCode.NO_TESTS_COLLECTED}:
        print(f"tests FAILED ({ex})")
        sys.exit(1)
    else:
        print("tests PASSED")

    #  Actual input data generally has more iterations, turn off log
    ic.disable()
    my_input = Path("input.txt").read_text().strip()
    result = solve(my_input)
    print(result)
