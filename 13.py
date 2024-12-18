from __future__ import annotations

import io
import re
import sys
from pathlib import Path
from typing import Protocol, cast, SupportsInt

# a1.x + b1.y + c1 = 0
# a2.x + b2.y + c2 = 0
#
# But in this case:
#   a1 = ΔX pressing button A
#   b1 = ΔX pressing button B
#   c1 = negative of wanted X
#
# While the .2 variants refer to ΔY and wanted Y

# fmt: off
TEST_SOLVER_EXPECT = [
    (94, 22,  8400, 34, 67,  5400, (80, 40)),
    (26, 67, 12748, 66, 21, 12176, None),
    (17, 84,  7870, 86, 37,  6450, (38, 86)),
    (69, 27, 18641, 33, 71, 10279, None),
]
# fmt: on

TEST_VECTOR = """\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""
TEST_EXPECT_1 = 480


class SupportIsInteger(Protocol):
    def is_integer(self) -> bool: ...


def linear_solve(a1, b1, c1, a2, b2, c2) -> tuple | None:
    denom = a1 * b2 - a2 * b1
    if not denom:
        return None
    x = (b1 * c2 - b2 * c1) / denom
    y = (c1 * a2 - c2 * a1) / denom
    return x, y


def aoc_solve(a1, b1, nc1, a2, b2, nc2) -> tuple[int, int] | None:
    result = linear_solve(a1, b1, -nc1, a2, b2, -nc2)
    if result is None:
        return None
    x: SupportIsInteger | SupportsInt
    y: SupportIsInteger | SupportsInt
    x, y = result
    if not x.is_integer() or not y.is_integer():
        return None
    return int(x), int(y)


def aoc_solve2(a1, b1, nc1, a2, b2, nc2) -> tuple[int, int] | None:
    result = linear_solve(a1, b1, -10000000000000 - nc1, a2, b2, -10000000000000 - nc2)
    if result is None:
        return None
    x: SupportIsInteger | SupportsInt
    y: SupportIsInteger | SupportsInt
    x, y = result
    if not x.is_integer() or not y.is_integer():
        return None
    return int(x), int(y)




RE_BUTTON = re.compile(r"Button (?P<btn>[AB]): X\+(?P<dx>\d+), Y\+(?P<dy>\d+)")
RE_PRIZE = re.compile(r"Prize: X=(?P<x>\d+), Y=(?P<y>\d+)")


def consume(stream):
    data: list[tuple[int, int, int, int, int, int]] = []
    bdx = []
    bdy = []
    for ln in stream:
        if not (ln := ln.strip()):
            continue
        if m := RE_BUTTON.match(ln):
            bdx.append(int(m.group("dx")))
            bdy.append(int(m.group("dy")))
            continue
        if m := RE_PRIZE.match(ln):
            data.append(
                (
                    bdx[0],
                    bdx[1],
                    int(m.group("x")),
                    bdy[0],
                    bdy[1],
                    int(m.group("y"))
                )
            )
            bdx.clear()
            bdy.clear()
            continue
        raise ValueError(f"Cannot parse: >{ln}<")
    return data


def _test():
    for a1, b1, nc1, a2, b2, nc2, expect in TEST_SOLVER_EXPECT:
        result = aoc_solve(a1, b1, nc1, a2, b2, nc2)
        print(f"Result: {result} , should be: {expect}")

    with io.StringIO(TEST_VECTOR) as fin:
        data = consume(fin)

    total = 0
    for item in data:
        result = aoc_solve(*item)
        if result is None:
            continue
        x, y = result
        # print(x, y)
        total += 3 * x + 1 * y
    print("Test 1-1:", total, "should be", TEST_EXPECT_1)
    assert total == TEST_EXPECT_1


def _main():
    data_file = Path(sys.argv[0]).with_suffix(".txt")
    with open(data_file, "rt") as fin:
        data = consume(fin)

    total = 0
    for item in data:
        result = aoc_solve(*item)
        if result is None:
            continue
        x, y = result
        # print(x, y)
        total += 3 * x + 1 * y
    print("Case 1:", total)

    total = 0
    for item in data:
        result = aoc_solve2(*item)
        if result is None:
            continue
        x, y = result
        # print(x, y)
        total += 3 * x + 1 * y
    print("Case 2:", total)


if __name__ == '__main__':
    _test()
    _main()
