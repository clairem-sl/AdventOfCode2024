from __future__ import annotations

import io
from itertools import combinations, pairwise


TEST_VECTOR = """\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""

TEST_RESULT_1 = 2
TEST_RESULT_2 = 4


def check_safe_1(seq: list[int]) -> bool:
    diffs = [(b - a) for a, b in pairwise(seq)]
    return all(1 <= d <= 3 for d in diffs) or all(-3 <= d <= -1 for d in diffs)


def check_safe_2(seq: list[int]) -> bool:
    return any(check_safe_1(dampened) for dampened in combinations(seq, len(seq) - 1))


def consume(stream) -> list[list[int]]:
    data: list[list[int]] = []
    for ln in stream:
        if not (ln := ln.strip()):
            continue
        data.append(list(map(int, ln.split())))
    return data


def _test():
    with io.StringIO(TEST_VECTOR) as fin:
        data = consume(fin)
    result = sum(check_safe_1(seq) for seq in data)
    print("Test Vector Case 1:", result)
    assert result == TEST_RESULT_1
    result = sum(check_safe_2(seq) for seq in data)
    print("Test Vector Case 2:", result)
    assert result == TEST_RESULT_2


def _main():
    with open("02.txt", "rt") as fin:
        data = consume(fin)
    result = sum(check_safe_1(seq) for seq in data)
    print("Actual Data Case 1:", result)
    result = sum(check_safe_2(seq) for seq in data)
    print("Actual Data Case 2:", result)


if __name__ == "__main__":
    _test()
    _main()
