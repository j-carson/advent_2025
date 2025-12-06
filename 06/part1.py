import sys
from functools import reduce
from pathlib import Path

import numpy as np
import pytest
from icecream import ic

# --> Puzzle solution


def split_problems(input_data: str):
    return np.array([row.split() for row in input_data.splitlines()]).T


def solve_problem(column):
    numbers = [int(i) for i in column[:-1]]

    match column[-1]:
        case "*":
            score = reduce(lambda x, y: x * y, numbers, 1)
        case "+":
            score = reduce(lambda x, y: x + y, numbers, 0)

    ic(numbers, score)
    return score


def solve(input_data):
    score = 0
    problems = split_problems(input_data)
    for column in problems:
        score += solve_problem(column)

    return score


# --> Test driven development helpers


# Test any examples given in the problem

sample_input = Path("input-sample.txt").read_text().strip()
EXAMPLES = [
    (sample_input, 4277556),
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
