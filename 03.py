from __future__ import annotations

import io
import re

TEST_VECTOR_1 = """\
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
"""
TEST_RESULT_1 = 161

TEST_VECTOR_2 = """\
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
"""
TEST_RESULT_2 = 48

RE_MUL = re.compile(r"mul\((\d+),(\d+)\)")
RE_OP = re.compile(r"do\(\)|don't\(\)|mul\((\d+),(\d+)\)")


def calculate_1(s: str) -> int:
    m: re.Match
    acc = 0
    for m in RE_MUL.finditer(s):
        a = int(m.group(1))
        b = int(m.group(2))
        acc += a * b
    return acc


def calculate_2(s: str) -> int:
    m: re.Match
    acc = 0
    do = True
    for m in RE_OP.finditer(s):
        match m.group(0):
            case "do()":
                do = True
            case "don't()":
                do = False
            case _:
                if do:
                    a = int(m.group(1))
                    b = int(m.group(2))
                    acc += a * b
    return acc


def consume(stream) -> str:
    lines = []
    for ln in stream:
        add_nl = ln.endswith("\n")
        if not (ln := ln.strip()):
            continue
        lines.append(ln)
        if add_nl:
            lines.append("\n")
    return "".join(lines)


def _test():
    with io.StringIO(TEST_VECTOR_1) as fin:
        data = consume(fin)
    result = calculate_1(data)
    print("Test Vector Case 1:", result)
    assert result == TEST_RESULT_1

    with io.StringIO(TEST_VECTOR_2) as fin:
        data = consume(fin)
    result = calculate_2(data)
    print("Test Vector Case 2:", result)
    assert result == TEST_RESULT_2


def _main():
    with open("03.txt", "rt") as fin:
        data = consume(fin)
    result = calculate_1(data)
    print("Actual Data Case 1:", result)
    result = calculate_2(data)
    print("Actual Data Case 2:", result)


if __name__ == "__main__":
    _test()
    _main()
