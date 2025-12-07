import sys
from functools import cache
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


class TachyonField:
    def __init__(self, input_text):
        self.field, self.start_index = read_input(input_text)
        self.nrow = self.field.shape[0]

    @cache
    def solve_one(self, start_index, current_depth):
        if current_depth >= self.nrow:
            return 1

        field = self.field[current_depth:, :]
        if field[0, start_index]:
            return self.solve_one(start_index + 1, current_depth + 1) + self.solve_one(
                start_index - 1, current_depth + 1
            )
        return self.solve_one(start_index, current_depth + 1)

    def solve(self):
        return self.solve_one(self.start_index, 0)


def solve(input_data):
    field = TachyonField(input_data)
    return field.solve()


# --> Test driven development helpers


# Test any examples given in the problem

sample_input = Path("input-sample.txt").read_text().strip()
EXAMPLES = [
    (sample_input, 40),
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
