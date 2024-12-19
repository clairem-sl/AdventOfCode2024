from __future__ import annotations

import io
import itertools
import operator

# noinspection PyUnresolvedReferences
import pprint  # noqa: F401

from collections.abc import Callable
from enum import Enum, auto
from typing import Final

from aoc2024_common import Point, open_puzzle_input

TEST_VECTOR_1: Final[str] = """\
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
"""
TEST_EXPECT_1_1: Final[int] = (21 * 36) + (4 * (1 * 4))
# TEST_EXPECT_1_1: Final[int] = 772
TEST_EXPECT_1_2: Final[int] = (21 * (4 + 4 * 4)) + (4 * (1 * 4))
# TEST_EXPECT_1_2: Final[int] = 436

TEST_VECTOR_2: Final[str] = """\
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""
TEST_EXPECT_2_1: Final[int] = 1930
TEST_EXPECT_2_2: Final[int] = 1206

TEST_VECTOR_3: Final[str] = """\
EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
"""
TEST_EXPECT_3_2: Final[int] = 236

TEST_VECTOR_4: Final[str] = """\
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
"""
TEST_EXPECT_4_2: Final[int] = 368


DIRS: Final[list[Point]] = [Point(1, 0), Point(0, 1), Point(-1, 0), Point(0, -1)]


def patches_by_species(matrix: list[str]) -> dict[str, list[set[Point]]]:
    garden: list[list[str | None]] = [list(row) for row in matrix]
    patches: dict[str, list[set[Point]]] = {}

    def _get_connected(spc: str, coord: Point) -> list:
        if (_s := coord @ garden) is None or _s != spc:
            return []
        garden[coord.y][coord.x] = None
        result = [coord]
        for _dir in DIRS:
            result.extend(_get_connected(spc, coord + _dir))
        return result

    for y, row in enumerate(garden):
        for x, species in enumerate(row):
            if species is None:
                continue
            patches.setdefault(species, []).append(
                set(_get_connected(species, Point(x, y)))
            )

    return patches


def calc_price(patches: list[set[Point]]) -> int:
    total = 0
    for patch in patches:
        area = len(patch)
        perimeter = 0
        for coord in patch:
            perimeter += sum((coord + _dir) not in patch for _dir in DIRS)
        # print(f"{area = }, {perimeter = }")
        total += area * perimeter
    return total


class CornerType(Enum):
    ConvexUL = auto()
    ConvexUR = auto()
    ConvexDL = auto()
    ConvexDR = auto()
    ConcaveUL = auto()
    ConcaveUR = auto()
    ConcaveDL = auto()
    ConcaveDR = auto()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


CORNER_DIRS: dict[CornerType, dict[Point, Callable[[str, str], bool]]] = {
    CornerType.ConvexUL: {
        Point(0, -1): operator.ne,
        Point(-1, 0): operator.ne,
    },
    CornerType.ConvexUR: {
        Point(0, -1): operator.ne,
        Point(1, 0): operator.ne,
    },
    CornerType.ConvexDL: {
        Point(0, 1): operator.ne,
        Point(-1, 0): operator.ne,
    },
    CornerType.ConvexDR: {
        Point(0, 1): operator.ne,
        Point(1, 0): operator.ne,
    },
    CornerType.ConcaveUL: {
        Point(-1, -1): operator.ne,
        Point(0, -1): operator.eq,
        Point(-1, 0): operator.eq,
    },
    CornerType.ConcaveUR: {
        Point(1, -1): operator.ne,
        Point(0, -1): operator.eq,
        Point(1, 0): operator.eq,
    },
    CornerType.ConcaveDL: {
        Point(-1, 1): operator.ne,
        Point(0, 1): operator.eq,
        Point(-1, 0): operator.eq,
    },
    CornerType.ConcaveDR: {
        Point(1, 1): operator.ne,
        Point(0, 1): operator.eq,
        Point(1, 0): operator.eq,
    },
}


def find_corners(matrix: list[str], all_patches: dict[str, list[set[Point]]]):
    corners: dict[str, dict[Point, list[CornerType]]] = {}
    for species, patches in all_patches.items():
        pos: Point
        for pos in itertools.chain.from_iterable(patches):
            for ctype, ctests in CORNER_DIRS.items():
                if all(
                    test(species, (pos + delta) @ matrix)
                    for delta, test in ctests.items()
                ):
                    # print(f"{pos} {ctype}")
                    corners.setdefault(species, {}).setdefault(pos, []).append(ctype)
    return corners


def calc_price2(
    all_patches: dict[str, list[set[Point]]],
    all_corners: dict[str, dict[Point, list[CornerType]]],
):
    total = 0
    for species, patches in all_patches.items():
        sp_corners = all_corners[species]
        for patch in patches:
            area = len(patch)
            sides = sum(len(sp_corners[pos]) for pos in patch if pos in sp_corners)
            total += area * sides
    return total


def consume(stream) -> list[str]:
    data = []
    for ln in stream:
        if not (ln := ln.strip()):
            continue
        data.append(ln)
    return data


def _test():
    def _runtest(
        label: str, test_vector: str, expect1: int | None, expect2: int | None
    ):
        with io.StringIO(test_vector) as fin:
            data = consume(fin)
        plots = patches_by_species(data)

        if expect1 is not None:
            result = sum(calc_price(coverage) for coverage in plots.values())
            print(f"Test {label}-1:", result, f"(should be {expect1})")
            assert result == expect1

        if expect2 is not None:
            all_corners = find_corners(data, plots)
            # pprint.pprint(all_corners)
            result = calc_price2(plots, all_corners)
            print(f"Test {label}-2:", result, f"(should be {expect2})")
            assert result == expect2

    _runtest("1", TEST_VECTOR_1, TEST_EXPECT_1_1, TEST_EXPECT_1_2)

    _runtest("2", TEST_VECTOR_2, TEST_EXPECT_2_1, TEST_EXPECT_2_2)

    _runtest("3", TEST_VECTOR_3, None, TEST_EXPECT_3_2)

    _runtest("4", TEST_VECTOR_4, None, TEST_EXPECT_4_2)

    print("===== All Tests Successful =====")


def _main():
    with open_puzzle_input() as fin:
        data = consume(fin)
    plots = patches_by_species(data)

    result = sum(calc_price(coverage) for coverage in plots.values())
    print("Case 1:", result)

    all_corners = find_corners(data, plots)
    result = calc_price2(plots, all_corners)
    print("Case 2:", result)


if __name__ == "__main__":
    _test()
    _main()
