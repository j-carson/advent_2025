import sys
from pathlib import Path

import numpy as np
import pytest
from icecream import ic

# --> Puzzle solution


def read_input(data):
    result = np.array(
        [[1 if c == "@" else 0 for c in row.strip()] for row in data.splitlines()],
        dtype=int,
    )
    ic(result, result.shape)
    return result


def solve(input_data):
    data_array = read_input(input_data)

    score = 0
    rows, cols = data_array.shape

    for r in range(rows):
        r_up = max(r - 1, 0)
        r_down = min(r + 1, rows - 1)

        for c in range(cols):
            if data_array[r, c]:
                c_left = max(c - 1, 0)
                c_right = min(c + 1, cols - 1)

                grid = data_array[r_up : r_down + 1, c_left : c_right + 1]
                ic(r, c, grid, np.sum(grid))

                if np.sum(data_array[r_up : r_down + 1, c_left : c_right + 1]) < 5:
                    score += 1
    return score


# --> Test driven development helpers


# Test any examples given in the problem

sample_input = Path("input-sample.txt").read_text().strip()
EXAMPLES = [
    (sample_input, 13),
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
