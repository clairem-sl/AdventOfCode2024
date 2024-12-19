from __future__ import annotations

import io
import re

from typing import Final, TYPE_CHECKING

from aoc2024_common import open_puzzle_input

TEST_VECTOR: Final[str] = """\
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""

TEST_RESULT_1: Final[int] = 143
TEST_RESULT_2: Final[int] = 123


if TYPE_CHECKING:
    RulesDict = dict[tuple[str, str], re.Pattern]


def is_correct_order(rules: list[tuple[str, str]], line: list[str]) -> bool:
    applicable = 0
    correct = 0
    for a, b in rules:
        if a not in line or b not in line:
            continue
        applicable += 1
        correct += line.index(a) < line.index(b)
    return correct == applicable


def check_1(rules: list[tuple[str, str]], data: list[list[str]]) -> int:
    # fmt: off
    valid: list[list[str]] = [
        ln
        for ln in data
        if is_correct_order(rules, ln)
    ]
    # fmt: on
    return sum(int(v[len(v) // 2]) for v in valid)


def check_2(rules: list[tuple[str, str]], data: list[list[str]]) -> int:
    # fmt: off
    invalid: list[list[str]] = [
        ln
        for ln in data
        if not is_correct_order(rules, ln)
    ]
    # fmt: on
    corrected: list[list[str]] = []
    ln: list[str]
    for ln in invalid:
        # We're basically doing Exchange Sort here
        while not is_correct_order(rules, ln):
            for a, b in rules:
                if a not in ln or b not in ln:
                    continue
                ia, ib = ln.index(a), ln.index(b)
                if ia > ib:
                    ln[ia], ln[ib] = ln[ib], ln[ia]
        corrected.append(ln)
    return sum(int(ln[len(ln) // 2]) for ln in corrected)


def consume(stream) -> tuple[list[tuple[str, str]], list[list[str]]]:
    rules: list[tuple[str, str]] = []
    data: list[list[str]] = []
    for ln in stream:
        if not (ln := ln.strip()):
            continue
        if "|" in ln:
            a, b = ln.split("|")
            rules.append((a, b))
        else:
            data.append(ln.split(","))
    return rules, data


def _test():
    with io.StringIO(TEST_VECTOR) as fin:
        rules2, data2 = consume(fin)

    result = check_1(rules2, data2)
    print("Test Vector Case 1:", result)
    assert result == TEST_RESULT_1

    result = check_2(rules2, data2)
    print("Test Vector Case 2:", result)
    assert result == TEST_RESULT_2


def _main():
    with open_puzzle_input() as fin:
        rules2, data2 = consume(fin)

    result = check_1(rules2, data2)
    print("Actual Data Case 1:", result)

    result = check_2(rules2, data2)
    print("Actual Data Case 2:", result)


if __name__ == "__main__":
    _test()
    _main()
