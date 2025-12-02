import sys
from pathlib import Path

import numpy as np
import pytest
from icecream import ic

# --> Puzzle solution


def round_up(val: str) -> str:
    """Round up an odd-length value to the closest even one"""
    if len(val) % 2 == 0:
        return val
    return "1" + "0" * len(val)


def test_round_up():
    assert round_up("998") == "1000"


def round_down(val: str) -> str:
    """Round up an odd-length value to the closest even one"""
    if len(val) % 2 == 0:
        return val
    return "9" * (len(val) - 1)


def test_round_down():
    assert round_down("998") == "99"


class Range:
    def __init__(self, product_ids):
        low, high = product_ids.split("-")
        low_val = int(low)
        high_val = int(high)

        # Fallback value
        self.matches = []

        low_str = round_up(low)
        high_str = round_down(high)
        if int(low_str) > int(high_str):
            return

        len_low = len(low_str)
        search_start = int(low_str[: len_low // 2])

        len_high = len(high_str)
        search_stop = int(high_str[: len_high // 2])

        for k in range(search_start, search_stop + 1):
            test_val = int(str(k) * 2)
            if low_val <= test_val <= high_val:
                self.matches.append(test_val)
            if test_val > high_val:
                return

    def score(self):
        if self.matches:
            return np.sum(self.matches)
        return 0


def solve(input_data):
    total_score = 0
    for item in input_data.split(","):
        total_score += Range(item).score()

    return total_score


# --> Test driven development helpers


# Test any examples given in the problem

sample_input = Path("sample.txt").read_text().strip()
EXAMPLES = [
    (sample_input, 1227775554),
]


@pytest.mark.parametrize(
    "single_example,single_solution",
    zip(
        sample_input.split(","),
        [[11, 22], [99], [1010], [1188511885], [222222], [], [446446], [38593859], []],
    ),
)
def test_single_example(single_example, single_solution):
    assert Range(single_example).matches == single_solution


@pytest.mark.parametrize("sample_data,sample_solution", EXAMPLES, ids=("sample",))
def test_samples(sample_data, sample_solution) -> None:
    assert solve(sample_data) == sample_solution


# --> Setup and run

if __name__ == "__main__":
    #  Run the test examples with icecream debug-trace turned on
    ic.enable()
    ex = pytest.main([__file__, "--capture=tee-sys", "-v", "--pdb"])
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
