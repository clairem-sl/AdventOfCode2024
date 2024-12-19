from __future__ import annotations

import io
import itertools
import operator
import re

from collections import deque
from collections.abc import Callable
from typing import Final, TYPE_CHECKING

from aoc2024_common import open_puzzle_input

TEST_VECTOR: Final[str] = """\
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""
TEST_EXPECT_1: Final[int] = 3749
TEST_EXPECT_2: Final[int] = 11387


RE_PARSE: Final[re.Pattern] = re.compile(r"(?P<want>\d+):\s+(?P<rest>[\d\s]+)")


def consume(stream):
    data: list = []
    for ln in stream:
        ln = ln.strip()
        if (m := RE_PARSE.match(ln)) is None:
            continue
        want = int(m.group("want"))
        operands = [int(d) for d in m.group("rest").split()]
        data.append([want, operands])
    return data


if TYPE_CHECKING:
    IntOperator = Callable[[int, int], int]


def validate(want: int, operands: list[int], valid_ops: list[IntOperator]) -> bool:
    for opers in itertools.product(valid_ops, repeat=(len(operands) - 1)):
        _opnds = deque(operands)
        _oprs = deque(opers)
        accu = _opnds.popleft()
        while _opnds:
            _val = _opnds.popleft()
            _op = _oprs.popleft()
            accu = _op(accu, _val)
            # Since the valid operations always increases the value, if we have passed the wanted value, no
            # need to use the rest of the operators
            if accu > want:
                break
        if accu == want:
            return True
    return False


def concat(a: int, b: int) -> int:
    return int(f"{a}{b}")


VALID_OPS_1: Final[list[IntOperator]] = [
    operator.add,
    operator.mul,
]
VALID_OPS_2: Final[list[IntOperator]] = [
    operator.add,
    operator.mul,
    concat,
]


def _test():
    with io.StringIO(TEST_VECTOR) as fin:
        data = consume(fin)

    total = sum(
        want for want, operands in data if validate(want, operands, VALID_OPS_1)
    )
    print("Test 1:", total)
    assert total == TEST_EXPECT_1

    total = sum(
        want for want, operands in data if validate(want, operands, VALID_OPS_2)
    )
    print("Test 2:", total)
    assert total == TEST_EXPECT_2


def _main():
    with open_puzzle_input() as fin:
        data = consume(fin)

    total = sum(
        want for want, operands in data if validate(want, operands, VALID_OPS_1)
    )
    print("Case 1:", total)

    total = sum(
        want for want, operands in data if validate(want, operands, VALID_OPS_2)
    )
    print("Case 2:", total)


if __name__ == "__main__":
    _test()
    _main()
