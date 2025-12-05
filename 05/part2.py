import sys
from pathlib import Path

import pytest
from icecream import ic

# --> Puzzle solution


class Range:  # noqa: PLW1641
    def __init__(self, min_val, max_val):
        self.min, self.max = min_val, max_val

    def check(self, val):
        return self.min <= val <= self.max

    def __eq__(self, other):
        return self.min == other.min and self.max == other.max

    def __gt__(self, other):
        return (self.min > other.min) or (
            self.min == other.min and self.max > other.max
        )

    def __str__(self):
        return f"Range(min={self.min},max={self.max})"

    def __repr__(self):
        return f"Range(min={self.min},max={self.max})"

    def merge(self, other):
        if self.min <= other.min <= self.max:
            return Range(self.min, max(self.max, other.max))
        return None

    def __len__(self):
        return self.max - self.min + 1


def parse(input_data):
    ranges, _ = input_data.split("\n\n")
    result = []
    for row in ranges.splitlines():
        minv, maxv = [int(i) for i in row.split("-")]
        result.append(Range(minv, maxv))
    return sorted(result)


def try_merges(ranges):
    ic(ranges)
    result = []

    prev = ranges[0]
    for next_val in ranges[1:]:
        if merged := prev.merge(next_val):
            prev = merged
        else:
            result.append(prev)
            prev = next_val

    result.append(prev)
    ic(result)
    return result


def solve(input_data):
    ranges = parse(input_data)

    current_len = len(ranges)
    new_ranges = try_merges(ranges)

    while len(new_ranges) < current_len:
        current_len = len(new_ranges)
        new_ranges = try_merges(new_ranges)

    return sum(len(r) for r in new_ranges)


# --> Test driven development helpers


# Test any examples given in the problem

sample_input = Path("input-sample.txt").read_text().strip()
EXAMPLES = [
    (sample_input, 14),
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
