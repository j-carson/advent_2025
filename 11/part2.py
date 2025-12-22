import sys
from collections import defaultdict
from functools import cache
from pathlib import Path

import pytest
from icecream import ic

# --> Puzzle solution


class Node:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    @cache
    def search(self, dest, visited):
        if dest == self.name:
            if ("fft" in visited) and ("dac" in visited):
                return 1
            return 0
        if self.name in {"fft", "dac"}:
            new_visit = frozenset({self.name}) | visited
        else:
            new_visit = visited
        return sum(child.search(dest, new_visit) for child in self.children)


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

        tree = {}
        for key, values in edges.items():
            if key not in tree:
                tree[key] = Node(key)
            for v in values:
                if v not in tree:
                    tree[v] = Node(v)
                tree[key].add_child(tree[v])
        self.tree = tree

    def solve(self):
        srv = self.tree["svr"]
        return srv.search("out", frozenset())


def solve(file_path):
    return Puzzle(file_path).solve()


# --> Test driven development helpers


# Test any examples given in the problem


@pytest.mark.parametrize("sample_data,sample_solution", [["input-sample.txt", 2]])
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
    result = solve("input.txt")
    print(result)
