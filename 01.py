from __future__ import annotations

import collections
import io

TEST_VECTOR = """\
3   4
4   3
2   5
1   3
3   9
3   3
"""

TEST_RESULT_1 = 11
TEST_RESULT_2 = 31


def consume(stream) -> tuple[list[int], list[int]]:
    left = []
    right = []
    for ln in stream:
        if not (ln := ln.strip()):
            continue
        l, r = ln.split()  # noqa: E741
        left.append(int(l))
        right.append(int(r))
    return left, right


def calculate_1(seq1, seq2):
    ss1 = sorted(seq1)
    ss2 = sorted(seq2)
    return sum(abs(left - right) for left, right in zip(ss1, ss2))


def calculate_2(seq1, seq2):
    cs2 = collections.Counter(seq2)
    return sum(left * cs2[left] for left in seq1)


def _test():
    with io.StringIO(TEST_VECTOR) as fin:
        left, right = consume(fin)
    result = calculate_1(left, right)
    print("Test Vector Case 1 :", result)
    assert result == TEST_RESULT_1
    result = calculate_2(left, right)
    print("Test Vector Case 2 :", result)
    assert result == TEST_RESULT_2


def _main():
    with open("01.txt", "rt") as fin:
        left, right = consume(fin)
    result = calculate_1(left, right)
    print("Actual Data Case 1:", result)
    with open("01.txt", "rt") as fin:
        left, right = consume(fin)
    result = calculate_2(left, right)
    print("Actual Data Case 2:", result)


if __name__ == "__main__":
    _test()
    _main()
