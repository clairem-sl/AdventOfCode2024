from __future__ import annotations

import sys
from functools import singledispatchmethod
from pathlib import Path
from typing import NamedTuple, Sequence, Self, TextIO


class Point(NamedTuple):
    x: int
    y: int

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other: int) -> Point:
        return Point(self.x * other, self.y * other)

    def __mod__(self, other: Point) -> Point:
        return Point(self.x % other.x, self.y % other.y)

    def __matmul__(self, matrix: Sequence[Sequence[str | None]]) -> str | None:
        if not (0 <= self.y < len(matrix)):
            return None
        line = matrix[self.y]
        if not (0 <= self.x < len(line)):
            return None
        return line[self.x]

    def __str__(self):
        return f"({self.x}, {self.y})"

    def shift_by(self, dx, dy) -> Self:
        """Return a Point after applying a shift (translate) transform"""
        return Point(self.x + dx, self.y + dy)

    def delta_to(self, other: Point) -> Point:
        """Calculate delta (signed shift) needed to translate to another Point. The values will be directional"""
        return Point(other.x - self.x, other.y - self.y)

    @singledispatchmethod
    def within(self, arg, *_):
        raise NotImplementedError(f"within() not defined for type {type(arg)}")

    @within.register
    def _(self, ubound_x: int, ubound_y: int, lbound_x: int = 0, lbound_y: int = 0):
        return (lbound_x <= self.x < ubound_x) and (lbound_y <= self.y < ubound_y)


# noinspection PyUnresolvedReferences
@Point.within.register
def _(self, corner1: Point, corner2: Point, inclusive_max: bool = False):
    xmin = min(corner1.x, corner2.x)
    xmax = max(corner1.x, corner2.x) + inclusive_max
    ymin = min(corner1.y, corner2.y)
    ymax = max(corner1.y, corner2.y) + inclusive_max
    return self.within(xmax, ymax, xmin, ymin)


def open_puzzle_input() -> TextIO:
    return open(Path(sys.argv[0]).with_suffix(".txt"))
