import sys
from pathlib import Path

import pytest
from icecream import ic

# --> Puzzle solution


class Battery:
    def __init__(self, bank):
        self.input = bank
        self.batteries = [int(i) for i in bank]

    def max_jolts(self):
        max_index = len(self.batteries) - 1
        for i in range(9, 0, -1):
            try:
                tens = self.batteries.index(i)
                if tens != max_index:
                    break
            except Exception:
                continue

        tens_val = self.batteries[tens]
        remainder = self.batteries[tens + 1 :]

        for i in range(9, 0, -1):
            try:
                ones = remainder.index(i)
                break
            except Exception:
                continue

        ones_val = remainder[ones]
        return tens_val * 10 + ones_val


def solve(input_data):
    score = 0
    for row in input_data.splitlines():
        batt = Battery(row.strip())
        score += batt.max_jolts()
    return score


# --> Test driven development helpers


# Test any examples given in the problem

sample_input = Path("sample.txt").read_text().strip()
EXAMPLES = [
    (sample_input, 357),
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
