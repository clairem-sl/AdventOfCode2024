from __future__ import annotations

import io
import itertools

from typing import Final

from aoc2024_common import open_puzzle_input

TEST_VECTOR = """\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""
TEST_EXPECT_1 = 41
TEST_EXPECT_2 = 6


def consume(stream):
    obstructions: set[tuple[int, int]] = set()
    guard_start: tuple[int, int] = -1, -1
    dim_x: int = 0
    dim_y: int = 0
    for y, ln in enumerate(stream):
        ln = ln.strip()
        if not ln:
            continue
        dim_y += 1
        dim_x = max(dim_x, len(ln))
        for x, c in enumerate(ln):
            match c:
                case "#":
                    obstructions.add((x, y))
                case "^":
                    if guard_start != (-1, -1):
                        raise ValueError("More than one guard!")
                    guard_start = x, y
    print(f"Field dimensions: {dim_x} x {dim_y}")
    return dim_x, dim_y, obstructions, guard_start


DIRECTIONS: Final[list[tuple[int, int]]] = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0),
]


def walk_map(
    dim_x, dim_y, obstructions: set[tuple[int, int]], guard_start: tuple[int, int]
):
    passed: dict[tuple[int, int], set[tuple[int, int]]] = {}
    x, y = guard_start
    for dir_ in itertools.cycle(DIRECTIONS):
        while True:
            dx, dy = dir_
            nx = x + dx
            ny = y + dy
            if (nx, ny) in obstructions:
                break
            passed.setdefault((x, y), set()).add(dir_)
            if not ((0 <= nx < dim_x) and (0 <= ny < dim_y)):
                return passed
            x, y = nx, ny
            # We have returned to a previously visited location and facing the same way
            # which means we have entered a loop
            if (x, y) in passed and dir_ in passed[x, y]:
                return None


def create_loop(
    dim_x, dim_y, obstructions: set[tuple[int, int]], guard_start: tuple[int, int]
):
    new_obstructions: set[tuple[int, int]] = set()
    ctr = itertools.count()
    found_ctr = itertools.count()
    for y in range(dim_y):
        for x in range(dim_x):
            if next(ctr) % 100 == 0:
                print(".", end="", flush=True)
            trypos = x, y
            if trypos == guard_start or trypos in obstructions:
                continue
            tryobs = obstructions.copy()
            tryobs.add(trypos)
            if walk_map(dim_x, dim_y, tryobs, guard_start) is not None:
                continue
            if next(found_ctr) % 10 == 0:
                print("+", end="", flush=True)
            new_obstructions.add(trypos)
    print()
    return new_obstructions


def _test():
    with io.StringIO(TEST_VECTOR) as fin:
        dim_x, dim_y, obstructions, guard_start = consume(fin)
    passed = walk_map(dim_x, dim_y, obstructions, guard_start)
    result = len(passed)
    print("Test 1:", result)
    assert result == TEST_EXPECT_1

    print("Calculating Test 2 ...", end="")
    new_obstructions = create_loop(dim_x, dim_y, obstructions, guard_start)
    result = len(new_obstructions)
    print("Test 2:", result)
    assert result == TEST_EXPECT_2


def _main():
    with open_puzzle_input() as fin:
        dim_x, dim_y, obstructions, guard_start = consume(fin)

    passed = walk_map(dim_x, dim_y, obstructions, guard_start)
    result = len(passed)
    print("Case 1:", result)

    print("Calculating Case 2 ...", end="")
    new_obstructions = create_loop(dim_x, dim_y, obstructions, guard_start)
    result = len(new_obstructions)
    print("Case 2:", result)


if __name__ == "__main__":
    _test()
    _main()
