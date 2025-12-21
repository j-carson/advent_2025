import sys
from functools import cache
from itertools import combinations, count
from pathlib import Path

import numpy as np
import pytest
from icecream import ic

# --> Puzzle solution


class Puzzle:
    def __init__(self, row):
        raw_pattern, *wiring, _ = row.split()
        self.pattern = np.array(
            [0 if ch == "." else 1 for ch in list(raw_pattern[1:-1])]
        )
        wiring_int = [{int(i) for i in wire[1:-1].split(",")} for wire in wiring]
        self.wiring = [
            np.array([1 if i in item else 0 for i in range(len(self.pattern))])
            for item in wiring_int
        ]

    @cache
    def try_toggles(self, state_tuple, button_order_tuple):
        state = np.array(state_tuple)
        state ^= self.wiring[button_order_tuple[0]]

        if len(button_order_tuple) == 1:
            return np.all(state == self.pattern)
        return self.try_toggles(tuple(state), button_order_tuple[1:])

    def score(self):
        empty_score = tuple(np.zeros_like(self.pattern))
        for c in count(1):
            for toggles in combinations(range(len(self.wiring)), c):
                if self.try_toggles(empty_score, toggles):
                    return c
        raise Exception("oops")


def solve(input_data):
    rows = input_data.splitlines()
    total_score = 0
    for row in rows:
        total_score += Puzzle(row).score()
    return total_score


# --> Test driven development helpers


# Test any examples given in the problem

sample_input = Path("input-sample.txt").read_text().strip()
EXAMPLES = [
    (sample_input, 7),
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
