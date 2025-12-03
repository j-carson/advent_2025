import sys
from pathlib import Path

import numpy as np
import pytest
from icecream import ic

# --> Puzzle solution


def round_up(val: str, n_repeats: int) -> str | None:
    """Round up an odd-length value to the closest one
    for a given pattern length"""

    lcm = np.lcm(len(val), n_repeats)
    if lcm == len(val):
        return val

    chunk_size = (len(val) // n_repeats) + 1
    new_len = n_repeats * chunk_size
    return "1" + "0" * (new_len - 1)


def test_round_up():
    assert round_up("998", 2) == "1000"
    assert round_up("998", 3) == "998"

    assert round_up("1998", 2) == "1998"
    assert round_up("1998", 3) == "100000"


def round_down(val: str, n_repeats: int) -> str:
    """Round down an odd-length value to the closest one for a
    given pattern length"""

    new_len = (len(val) // n_repeats) * n_repeats
    if new_len < len(val):
        return "9" * (len(val) - 1)
    return val


def test_round_down():
    assert round_down("998", 2) == "99"
    assert round_down("998", 3) == "998"
    assert round_down("1998", 3) == "999"


class Range:
    def __init__(self, product_ids):
        self.matches = []

        low, high = product_ids.split("-")
        low_val = int(low)
        high_val = int(high)

        solutions = set()

        max_repeats = max(len(low), len(high))
        for n_repeats in range(2, max_repeats + 1):
            low_str = round_up(low, n_repeats)
            high_str = round_down(high, n_repeats)

            if int(low_str) > int(high_str):
                continue

            len_low = len(low_str)
            search_start = int(low_str[: len_low // n_repeats])

            len_high = len(high_str)
            search_stop = int(high_str[: len_high // n_repeats])

            for k in range(search_start, search_stop + 1):
                test_val = int(str(k) * n_repeats)
                if low_val <= test_val <= high_val:
                    solutions.add(test_val)
                if test_val > high_val:
                    break

        self.matches = sorted(solutions)

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
    (sample_input, 4174379265),
]


@pytest.mark.parametrize(
    "single_example,single_solution",
    zip(
        sample_input.split(","),
        [
            [11, 22],
            [99, 111],
            [999, 1010],
            [1188511885],
            [222222],
            [],
            [446446],
            [38593859],
            [565656],
            [824824824],
            [2121212121],
        ],
    ),
)
def test_single_example(single_example, single_solution):
    puzzle = Range(single_example)
    assert puzzle.matches == single_solution
    pass
    pass


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
