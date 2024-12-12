from __future__ import annotations

import io
import sys
from functools import cache
from pathlib import Path
from typing import Final, NamedTuple, Sequence


TEST_VECTOR: Final[str] = """\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""
TEST_EXPECT_1: Final[int] = 36
TEST_EXPECT_2: Final[int] = 81


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __matmul__(self, matrix: Sequence[str]) -> int | None:
        if not (0 <= self.y < len(matrix)):
            return None
        line = matrix[self.y]
        if not (0 <= self.x < len(line)):
            return None
        return int(line[self.x])

    def __str__(self):
        return f"({self.x}, {self.y})"


DIRS = [
    Point(0, -1),
    Point(1, 0),
    Point(0, 1),
    Point(-1, 0),
]


@cache
def _find_trail_recurse(
        matrix: tuple[str, ...], so_far: tuple[Point, ...], max_val: int = 9
) -> tuple[tuple[Point, ...], ...]:
    cur_pos: Point = so_far[-1]
    cur_val: int = int(cur_pos @ matrix)
    if cur_val == max_val:
        return so_far,
    next_val = cur_val + 1
    solutions = []
    for _dir in DIRS:
        try_pos = cur_pos + _dir
        if (try_val := try_pos @ matrix) is None:
            continue
        if try_val != next_val:
            continue
        next_trail = tuple(list(so_far) + [try_pos])
        for solution in _find_trail_recurse(matrix, next_trail, max_val):
            solutions.append(solution)
    return tuple(set(solutions))


def find_trails(matrix: tuple[str, ...]) -> dict[Point, list[tuple[Point, ...]]]:
    trails = []
    for y, ln in enumerate(matrix):
        for x, c in enumerate(ln):
            if c == "0":
                trails.extend(_find_trail_recurse(matrix, (Point(x, y),)))
    trails_by_head = {}
    for t in trails:
        trails_by_head.setdefault(t[0], []).append(t)
    return trails_by_head


def calc_trailscore(trails: list[tuple[Point, ...]]):
    ends = set(t[-1] for t in trails)
    return len(ends)


def calc_trailrating(trails: list[tuple[Point, ...]]):
    return len(trails)


def consume(stream) -> tuple[str, ...]:
    data: list[str] = []
    for ln in stream:
        if not (ln := ln.strip()):
            continue
        data.append(ln)
    return tuple(data)


def _test():
    with io.StringIO(TEST_VECTOR) as fin:
        data = consume(fin)

    trails = find_trails(data)

    result = sum(calc_trailscore(t) for t in trails.values())
    print("Test 1:", result)
    assert result == TEST_EXPECT_1

    result = sum(calc_trailrating(t) for t in trails.values())
    print("Test 2:", result)
    assert result == TEST_EXPECT_2


def _main():
    data_file = Path(sys.argv[0]).with_suffix(".txt")
    with open(data_file, "rt") as fin:
        data = consume(fin)

    trails = find_trails(data)

    result = sum(calc_trailscore(t) for t in trails.values())
    print("Case 1:", result)

    result = sum(calc_trailrating(t) for t in trails.values())
    print("Case 1:", result)


if __name__ == '__main__':
    _test()
    _main()
