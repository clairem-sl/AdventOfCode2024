from __future__ import annotations

import io
from enum import IntEnum
from itertools import product
from typing import Final


TEST_VECTOR: Final[str] = """\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""
TEST_RESULT_1: Final[int] = 18
TEST_RESULT_2: Final[int] = 9


class ScanDir(IntEnum):
    dec = -1
    stay = 0
    inc = 1


def count_xmas(matrix: list[str]) -> int:

    def check_mas(sx, sy, dir_x: ScanDir, dir_y: ScanDir) -> bool:
        if dir_x == dir_y == ScanDir.stay:
            return False
        _x, _y = sx, sy
        try:
            for c in "MAS":
                _x += dir_x
                _y += dir_y
                # Prevent wraparound
                if _y < 0 or _x < 0:
                    return False
                if matrix[_y][_x] != c:
                    return False
        except IndexError:
            return False
        return True

    # fmt: off
    return sum(
        sum(
            check_mas(x, y, xd, yd)
            for xd, yd in product(iter(ScanDir), iter(ScanDir))
        )
        for y, row in enumerate(matrix)
        for x, char in enumerate(row)
        if char == "X"
    )
    # fmt: on


def count_crossmas(matrix: list[str]) -> int:
    lx: int
    ly: int

    _MS_PATT = {"MSMS", "MMSS", "SMSM", "SSMM"}

    def check_ms(sx, sy) -> bool:
        # fmt: off
        cross_patt = "".join(
            matrix[sy + dy][sx + dx]
            for dy in (-1, 1)
            for dx in (-1, 1)
        )
        # fmt: on
        return cross_patt in _MS_PATT

    accu = 0
    ly = len(matrix)
    for y in range(1, ly - 1):
        lx = len(matrix[y])
        for x in range(1, lx - 1):
            if matrix[y][x] != "A":
                continue
            accu += check_ms(x, y)

    return accu


def consume(stream) -> list[str]:
    data = []
    for ln in stream:
        if not (ln := ln.strip()):
            continue
        data.append(ln)
    return data


def _test():
    with io.StringIO(TEST_VECTOR) as fin:
        matrix = consume(fin)

    result = count_xmas(matrix)
    print("Test Vector Case 1:", result)
    assert result == TEST_RESULT_1

    result = count_crossmas(matrix)
    print("Test Vector Case 2:", result)
    assert result == TEST_RESULT_2


def _main():
    with open("04.txt", "rt") as fin:
        matrix = consume(fin)

    result = count_xmas(matrix)
    print("Actual Data Case 1:", result)

    result = count_crossmas(matrix)
    print("Actual Data Case 2:", result)


if __name__ == "__main__":
    _test()
    _main()
