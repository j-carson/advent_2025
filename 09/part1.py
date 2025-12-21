import sys
from pathlib import Path
from typing import NamedTuple

import numpy as np
import pytest
from icecream import ic

# --> Puzzle solution


class Point(NamedTuple):
    x: int
    y: int


class Rectangle(NamedTuple):
    p1: Point
    p2: Point

    def area(self):
        l1 = np.abs(self.p1.x - self.p2.x) + 1
        l2 = np.abs(self.p1.y - self.p2.y) + 1
        return l1 * l2


def read_data(input_data):
    result = []
    for row in input_data.splitlines():
        v1, v2 = row.split(",")
        result.append(Point(int(v1), int(v2)))
    ic(result)
    return result


def solve(input_data):
    max_area = 0
    points = read_data(input_data)

    for i, p1 in enumerate(points):
        for j, p2 in enumerate(points[i + 1 :]):
            if (area := Rectangle(p1, p2).area()) > max_area:
                max_area = area
    return max_area


# --> Test driven development helpers


# Test any examples given in the problem

sample_input = Path("input-sample.txt").read_text().strip()
EXAMPLES = [
    (sample_input, 50),
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
