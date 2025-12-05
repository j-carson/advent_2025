import sys
from pathlib import Path

import pytest
from icecream import ic

# --> Puzzle solution


class Range:
    def __init__(self, line):
        self.min, self.max = [int(i) for i in line.split("-")]

    def check(self, val):
        return self.min <= val <= self.max

    def __str__(self):
        return f"Range(min={self.min},max={self.max})"

    def __repr__(self):
        return f"Range(min={self.min},max={self.max})"


def parse(input_data):
    ranges, values = input_data.split("\n\n")

    range_obs = [Range(row) for row in ranges.splitlines()]
    value_list = [int(row) for row in values.splitlines()]

    return range_obs, value_list


def solve(input_data):
    ranges, values = parse(input_data)

    ic(ranges)
    ic(values)

    score = 0
    for value in values:
        for r in ranges:
            if r.check(value):
                ic("scored", value)
                score += 1
                break
    return score


# --> Test driven development helpers


# Test any examples given in the problem

sample_input = Path("input-sample.txt").read_text().strip()
EXAMPLES = [
    (sample_input, 3),
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
