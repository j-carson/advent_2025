from __future__ import annotations

from itertools import pairwise
from pathlib import Path
from typing import NamedTuple

# --> Puzzle solution


class Point(NamedTuple):
    x: int
    y: int


class Line:
    __slots__ = [
        "is_horizontal",
        "is_vertical",
        "length",
        "p1",
        "p2",
        "x_range",
        "y_range",
    ]

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

        self.is_horizontal = self.p1.y == self.p2.y
        self.is_vertical = self.p1.x == self.p2.x
        assert sum([self.is_horizontal, self.is_vertical]) == 1

        self.y_range = sorted((self.p1.y, self.p2.y))
        self.x_range = sorted((self.p1.x, self.p2.x))

        self.length = (
            max(
                self.x_range[1] - self.x_range[0],
                self.y_range[1] - self.y_range[0],
            )
            + 1
        )


class Rectangle:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.min_x, self.max_x = sorted([self.p1.x, self.p2.x])
        self.min_y, self.max_y = sorted([self.p1.y, self.p2.y])
        l1 = self.max_x - self.min_x + 1
        l2 = self.max_y - self.min_y + 1
        self.area = l1 * l2

    def contains_point(self, p1):
        return (self.min_x < p1.x < self.max_x) and (self.min_y < p1.y < self.max_y)


class Puzzle:
    def __init__(self, points):
        self.points = points
        self.corners = set(points)
        self.make_outline(points)

    def make_outline(self, points):
        self.outline = []

        for p1, p2 in pairwise(points):
            self.outline.append(Line(p1, p2))

        p1 = points[0]
        p2 = points[-1]
        self.outline.append(Line(p1, p2))

    def two_long_lines(self):
        # Find the two long horizontal lines from the plot
        # and return them in sorted order by y
        lengths = sorted(
            ((ll.length, i) for i, ll in enumerate(self.outline)), reverse=True
        )

        s1, s2 = lengths[:2]
        l1 = self.outline[s1[1]]
        l2 = self.outline[s2[1]]
        if l1.p1.y > l2.p1.y:
            return [l2, l1]
        return [l1, l2]

        return [ll[0] for ll in lengths[:2]]

    def solve(self):
        # Find the two long horizontal lines
        l1, l2 = self.two_long_lines()

        # segment the problem space into two parts
        # based on the cut-through in the middle of the circle
        y1 = l1.p1.y
        low_points = [p for p in self.points if p.y <= y1]

        y2 = l2.p1.y
        high_points = [p for p in self.points if p.y >= y2]

        # Solve each half separately
        m1 = get_max_rect(low_points)
        m2 = get_max_rect(high_points)
        return max(m1, m2)


def get_max_rect(points):
    all_rects = [
        Rectangle(p1, p2) for i, p1 in enumerate(points) for p2 in points[i + 1 :]
    ]
    all_areas = sorted(((r.area, i) for i, r in enumerate(all_rects)), reverse=True)
    for a, i in all_areas:
        valid = True
        r = all_rects[i]
        for p in points:
            if r.contains_point(p):
                valid = False
                break
        if valid:
            return a
    raise Exception("oops")


def solve(input_data):
    points = read_data(input_data)
    puzzle = Puzzle(points)
    print(puzzle.solve())


def read_data(input_data):
    result = []
    for row in input_data.splitlines():
        v1, v2 = row.split(",")
        result.append(Point(int(v1), int(v2)))
    return result


if __name__ == "__main__":
    input_data = Path("input.txt").read_text()
    solve(input_data)
