from __future__ import annotations

import io
import itertools

from typing import Final

from aoc2024_common import Point, open_puzzle_input

TEST_VECTOR_1: Final[str] = """\
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""
TEST_EXPECT_1_1: Final[int] = 14
TEST_EXPECT_1_2: Final[int] = 34

TEST_VECTOR_2: Final[str] = """\
..A
.A.
...
"""
TEST_EXPECT_2_1: Final[int] = 1


def consume(stream):
    antennae: dict[str, set[Point]] = {}
    ln: str
    dim_x = dim_y = 0
    for ln in stream:
        if not (ln := ln.strip()):
            continue
        dim_x = max(dim_x, len(ln))
        for x, c in enumerate(ln):
            if c == ".":
                continue
            antennae.setdefault(c, set()).add(Point(x, dim_y))
        dim_y += 1
    return dim_x, dim_y, antennae


def find_antinodes(dim_x, dim_y, antennae: dict[str, set[Point]]):
    antinodes: set[Point] = set()
    for channel, positions in antennae.items():
        a1: Point
        a2: Point
        for a1, a2 in itertools.combinations(positions, 2):
            shift = a2 - a1
            an1 = a1 - shift
            an2 = a2 + shift
            if an1.within(dim_x, dim_y):
                antinodes.add(an1)
            if an2.within(dim_x, dim_y):
                antinodes.add(an2)
    return antinodes


def find_antinodes2(dim_x, dim_y, antennae: dict[str, set[Point]]):
    antinodes: set[Point] = set()
    for channel, positions in antennae.items():
        a1: Point
        a2: Point
        for a1, a2 in itertools.combinations(positions, 2):
            shift = a2 - a1
            an1 = a1
            while an1.within(dim_x, dim_y):
                antinodes.add(an1)
                an1 = an1 - shift
            an2 = a2
            while an2.within(dim_x, dim_y):
                antinodes.add(an2)
                an2 = an2 + shift
    return antinodes


def _test():
    a = Point(1, 1)
    b = Point(1, 1)
    assert a == b
    assert hash(a) == hash(b)
    # noinspection PyDictCreation
    d = {a: 123}
    d[b] = 345
    assert d[a] == 345
    print("Sanity test successful")

    with io.StringIO(TEST_VECTOR_1) as fin:
        dim_x, dim_y, antennae = consume(fin)

    antinodes = find_antinodes(dim_x, dim_y, antennae)
    result = len(antinodes)
    print("Test 1-1:", result)
    assert result == TEST_EXPECT_1_1

    antinodes = find_antinodes2(dim_x, dim_y, antennae)
    result = len(antinodes)
    print("Test 1-2:", result)
    assert result == TEST_EXPECT_1_2

    with io.StringIO(TEST_VECTOR_2) as fin:
        dim_x, dim_y, antennae = consume(fin)

    antinodes = find_antinodes(dim_x, dim_y, antennae)
    result = len(antinodes)
    print("Test 2-1:", result)
    assert result == TEST_EXPECT_2_1


def _main():
    with open_puzzle_input() as fin:
        dim_x, dim_y, antennae = consume(fin)

    antinodes = find_antinodes(dim_x, dim_y, antennae)
    result = len(antinodes)
    print("Case 1:", result)

    antinodes = find_antinodes2(dim_x, dim_y, antennae)
    result = len(antinodes)
    print("Case 2:", result)


if __name__ == "__main__":
    _test()
    _main()
