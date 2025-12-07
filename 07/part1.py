import sys
from pathlib import Path

import numpy as np
import pytest
from icecream import ic

# --> Puzzle solution


def read_input(input_text):
    rows = input_text.splitlines()
    inputs = np.array(
        [[1 if ch == "^" else 0 for ch in list(row)] for row in rows],
        dtype=int,
    )
    ic(inputs)
    start_index = (rows[0]).index("S")
    return inputs, start_index


def solve(input_data):
    field, start_index = read_input(input_data)

    tachyons = np.zeros_like(field[0])
    tachyons[start_index] = 1

    score = 0
    for row in field[1:]:
        hit = tachyons & row
        score += hit.sum()

        ic(tachyons, row, hit, hit.sum())

        left_shift = np.roll(hit, -1)
        left_shift[-1] = 0

        right_shift = np.roll(hit, 1)
        right_shift[0] = 0

        tachyons |= left_shift
        tachyons |= right_shift
        tachyons &= ~hit

    return score


# --> Test driven development helpers


# Test any examples given in the problem

sample_input = Path("input-sample.txt").read_text().strip()
EXAMPLES = [
    (sample_input, 21),
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
