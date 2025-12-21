import sys
from collections import defaultdict
from functools import cache
from pathlib import Path

import pytest
from icecream import ic

# --> Puzzle solution


class Puzzle:
    def __init__(self, file_name):
        data = Path(file_name).read_text()
        edges = defaultdict(list)
        for row in data.splitlines():
            for word in row.split():
                if word[-1] == ":":
                    key = word[:-1]
                else:
                    edges[key].append(word)
        self.edges = edges

    @cache
    def get_n_paths(self, cur_path):
        # If all my choices go backwards, return 0

        ic(cur_path)

        next_step = [dest for dest in self.edges[cur_path[-1]] if dest not in cur_path]
        if len(next_step) == 0:
            ic("No valid next steps")
            return 0

        result = 0
        for step in next_step:
            if step == "out":
                ic("reached out")
                result += 1
            else:
                result += self.get_n_paths((*cur_path, step))
        return result

    def solve(self):
        first_step = self.edges["you"]
        n_paths = 0
        for step in first_step:
            n_paths += self.get_n_paths(("you", step))
        return n_paths


def solve(file_path):
    return Puzzle(file_path).solve()


# --> Test driven development helpers


# Test any examples given in the problem


@pytest.mark.parametrize("sample_data,sample_solution", [["input-sample.txt", 5]])
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
    result = solve("input.txt")
    print(result)
