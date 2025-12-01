import sys
from pathlib import Path

import pytest
from icecream import ic

# --> Puzzle solution


class Dial:
    def __init__(self):
        self.pos = 50
        self.score = 0

    def move(self, command):
        signs = {"L": -1, "R": 1}

        ic(command)

        sign = signs[command[0]]
        distance = int(command[1:])

        # score the full laps first
        self.score += distance // 100
        distance = distance % 100

        # you have to be off of zero to cross it
        if self.pos != 0:
            if (sign < 0) and (distance > self.pos):
                ic("left case")
                self.score += 1
            elif (sign > 0) and (distance + self.pos > 100):
                ic("right case")
                self.score += 1

        self.pos = (self.pos + sign * distance) % 100
        if self.pos == 0:
            ic("zero case")
            self.score += 1

        ic(self.__dict__)


def solve(input_data):
    dial = Dial()
    for row in input_data.splitlines():
        dial.move(row)
    return dial.score


# --> Test driven development helpers


# Test any examples given in the problem

sample_input = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""

EXAMPLES = [
    (sample_input, 6),
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
