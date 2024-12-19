from __future__ import annotations

import io
import math
import re
import sys

from collections import Counter
from pathlib import Path
from typing import NamedTuple

from aoc2024_common import Point

TEST_VECTORa = """\
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""

TEST_VECTORb = 11, 7

TEST_EXPECT_1 = """\
......2..1.
...........
1..........
.11........
.....1.....
...12......
.1....1....
"""

TEST_EXPECT_2 = 1, 3, 4, 1
TEST_EXPECT_3 = 12


class Robot(NamedTuple):
    start: Point
    velo: Point


def final_location(starting_data: list[Robot], dimension: Point, time_passed: int) -> list[Point]:
    final_pos = [
        (r.start + (r.velo * time_passed)) % dimension
        for r in starting_data
    ]
    return final_pos


def count_quadrant(final_pos: list[Point], dimension: Point):
    mid_x = dimension.x // 2
    mid_y = dimension.y // 2
    q1 = q2 = q3 = q4 = 0
    for x, y in final_pos:
        if x == mid_x or y == mid_y:
            continue
        match (0 <= x < mid_x, 0 <= y < mid_y):
            case True, True:
                q1 += 1
            case False, True:
                q2 += 1
            case True, False:
                q3 += 1
            case False, False:
                q4 += 1
    return q1, q2, q3, q4


def has_christmas_tree(final_pos: list[Point], depth: int = 5) -> bool:
    points = set(final_pos)
    seen = set()
    possibles = set()
    count = 0
    for one in final_pos:
        if one in seen:
            continue
        possibles.add(one)
        # Checking for triangle
        for shift in range(1, depth + 5):
            for dx in range(1, shift + 1):
                if (_r := one.shift_by(dx, shift)) not in points or \
                    (_l := one.shift_by(-dx, shift)) not in points:
                    break
                if _r in seen or _l in seen:
                    break
                possibles.add(_r)
                possibles.add(_l)
            else:
                # If we reach this point all dx 'seem' to be valid,
                # so we go into next shift
                continue
            # If we reached this that means we 'broke out' of the dx loop, and
            # that means what we've been scanning is not possible to be a xmas tree
            possibles.clear()
            break
        else:
            # If w reached this then we have successfully verified there's a triangle
            seen.update(possibles)
            count += 1
    if count > 3:
        return True


def has_christmas_tree2(final_pos: list[Point], dimension: Point) -> bool:
    allpos = set(final_pos)
    dump = []
    for y in range(dimension.y):
        for x in range(dimension.x):
            dump.append("1" if Point(x,y) in allpos else " ")
    dumps = "".join(dump)
    del dump
    patt1 = "1" * 21
    rslt1 = re.findall(patt1, dumps)
    if len(rslt1) < 3:
        return False
    patt2 = fr"1.{{{dimension.x - 1}}}1"
    rslt2 = re.findall(patt2, dumps)
    if len(rslt2) < 10:
        return False
    return True


RE_PARSER = re.compile(r"p=(?P<sx>\d+),(?P<sy>\d+) v=(?P<vx>-?\d+),(?P<vy>-?\d+)")


def consume(stream):
    data: list[Robot] = []
    for ln in stream:
        if not (ln := ln.strip()):
            continue
        if not (m := RE_PARSER.match(ln)):
            raise ValueError(f"Cannot parse {ln!r}")
        data.append(
            Robot(
                Point(int(m.group("sx")), int(m.group("sy"))),
                Point(int(m.group("vx")), int(m.group("vy"))),
            )
        )
    return data


def _test():
    with io.StringIO(TEST_VECTORa) as fin:
        data = consume(fin)

    dimension = Point(*TEST_VECTORb)
    final_pos = final_location(data, dimension, 100)
    count = count_quadrant(final_pos, dimension)
    print(f"Quadrants: {count}", f"should be {TEST_EXPECT_2}")
    assert count == TEST_EXPECT_2
    safety = math.prod(count)
    print("Safety factor:", safety, "should be", TEST_EXPECT_3)
    assert safety == TEST_EXPECT_3

    print("===== All Tests Passed =====")


def _main():
    data_file = Path(sys.argv[0]).with_suffix(".txt")
    with open(data_file, "rt") as fin:
        data = consume(fin)

    dimension = Point(101, 103)
    final_pos = final_location(data, dimension, 100)
    count = count_quadrant(final_pos, dimension)
    print(f"Quadrants: {count}")
    safety = math.prod(count)
    print("Safety factor:", safety)

    print("Looking for Christmas Tree ...", end=".", flush=True)
    count = 0
    while True:
        count += 1
        if (count % 100) == 0:
            print(".", end="", flush=True)
        final_pos = final_location(data, dimension, count)
        if has_christmas_tree2(final_pos, dimension):
            break
    print("\nChristmas Tree possibly seen at", count)


if __name__ == '__main__':
    _test()
    _main()
