import sys
from pathlib import Path

import pytest
from icecream import ic

# --> Puzzle solution


def max_jolts(bank, target_length):
    while len(bank) > target_length:
        for i in range(1, len(bank)):
            if bank[i] > bank[i - 1]:
                bank = bank[: i - 1] + bank[i:]
                break
        else:
            break

    return bank[:target_length]


def solve_one(row):
    bank = [int(i) for i in row.strip()]
    final_bank = max_jolts(bank, 12)
    return int("".join(str(i) for i in final_bank))


def solve(input_data):
    total_score = 0
    for row in input_data.splitlines():
        total_score += solve_one(row)
    return total_score


# --> Test driven development helpers


def test_examples():
    assert solve_one("987654321111111") == 987654321111
    assert solve_one("811111111111119") == 811111111119
    assert solve_one("234234234234278") == 434234234278
    assert solve_one("818181911112111") == 888911112111


# Test any examples given in the problem

sample_input = Path("sample.txt").read_text().strip()
EXAMPLES = [
    (sample_input, 3121910778619),
]


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
