import sys
from functools import reduce
from itertools import pairwise
from pathlib import Path

import numpy as np
import pytest
from icecream import ic

# --> Puzzle solution


def split_problems(input_data: str):
    rows = input_data.splitlines()
    first_rows = rows[:-1]
    last_row = rows[-1]

    start_cols = []
    for i, c in enumerate(last_row):
        if c in {"*", "+"}:
            start_cols.append(i)

    for left, right in pairwise(start_cols):
        numbers = [row[left : right - 1] for row in first_rows]
        yield numbers, last_row[left]

    numbers = [row[right:] for row in first_rows]
    yield numbers, last_row[-1]


def solve_problem(problem, operation):
    ic(problem)
    teed = np.rot90(np.array([list(n) for n in problem]))

    ic(teed)
    numbers = [int("".join(row)) for row in teed]
    ic(numbers, operation)

    match operation:
        case "*":
            score = reduce(lambda x, y: x * y, numbers, 1)
        case "+":
            score = reduce(lambda x, y: x + y, numbers, 0)

    return score


def solve(input_data):
    score = 0
    for numbers, operation in split_problems(input_data):
        score += solve_problem(numbers, operation)

    return score


# --> Test driven development helpers


# Test any examples given in the problem

sample_input = Path("input-sample.txt").read_text().strip()
EXAMPLES = [(sample_input, 3263827)]


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
