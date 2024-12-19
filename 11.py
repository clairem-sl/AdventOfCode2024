from __future__ import annotations

import io

from functools import cache
from typing import Final

from aoc2024_common import open_puzzle_input

TEST_VECTOR_1: Final[str] = """\
0 1 10 99 999
"""
TEST_EXPECT_1_1: Final[list[tuple[int, int]]] = [
    (1, 7),
]


TEST_VECTOR_2: Final[str] = """\
125 17
"""
TEST_EXPECT_2_1: Final[list[tuple[int, int]]] = [
    (1, 3),
    (2, 4),
    (3, 5),
    (4, 9),
    (5, 13),
    (6, 22),
    (25, 55312),
]


def mutate(original: list[int], blinks: int, multiplier: int = 2024):
    cur_list = original.copy()
    new_list: list[int]
    for _ in range(blinks):
        new_list = []
        for n in cur_list:
            if n == 0:
                new_list.append(1)
            elif (nl := len(ns := str(n))) % 2 == 0:
                mid = nl // 2
                new_list.append(int(ns[:mid]))
                new_list.append(int(ns[mid:]))
            else:
                new_list.append(multiplier * n)
        cur_list = new_list
    return cur_list


@cache
def count_mutations(seed: int, blinks: int, multiplier: int = 2024) -> int:
    if blinks == 0:
        return 1
    new_blinks = blinks - 1
    if seed == 0:
        return count_mutations(1, new_blinks, multiplier)
    elif (nl := len(ns := str(seed))) % 2 == 0:
        mid = nl // 2
        right = count_mutations(int(ns[mid:]), new_blinks, multiplier)
        return count_mutations(int(ns[:mid]), new_blinks, multiplier) + right
    else:
        return count_mutations(seed * multiplier, new_blinks, multiplier)


def consume(stream):
    data = []
    for ln in stream:
        if not (ln := ln.strip()):
            continue
        data.extend(ln.split())
    return [int(d) for d in data]


def _test():
    with io.StringIO(TEST_VECTOR_1) as fin:
        data = consume(fin)

    for blinks, expect in TEST_EXPECT_1_1:
        result = len(mutate(data, blinks))
        print(f"Test 1-{blinks}:", result)
        assert result == expect

    with io.StringIO(TEST_VECTOR_2) as fin:
        data = consume(fin)

    for blinks, expect in TEST_EXPECT_2_1:
        result = len(mutate(data, blinks))
        print(f"Test 2-{blinks}:", result)
        assert result == expect

    for blinks, expect in TEST_EXPECT_2_1:
        result = sum(count_mutations(seed, blinks) for seed in data)
        print(f"Test rec 2-{blinks}:", result)
        assert result == expect

    print("All Tests passed")


def _main():
    with open_puzzle_input() as fin:
        data = consume(fin)

    mutated = mutate(data, 25)
    result = len(mutated)
    print("Case 1:", result)
    del mutated

    # mutated = mutate(data, 75)
    # result = len(mutated)
    # print("Case 2:", result)
    # del mutated
    result = sum(count_mutations(seed, 75) for seed in data)
    print("Case 2:", result)


if __name__ == "__main__":
    _test()
    _main()
