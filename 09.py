from __future__ import annotations

import io
import itertools
import sys

from collections import deque
from pathlib import Path
from typing import Final


TEST_VECTOR: Final[str] = "2333133121414131402"
TEST_EXPECT_1: Final[int] = 1928
TEST_EXPECT_2: Final[int] = 2858


def consume(stream):
    raw = []
    ln: str
    for ln in stream:
        if not (ln := ln.strip()):
            continue
        raw.append(ln)
    return "".join(raw)


def build_disk_image(rle: str):
    disk: list[int | None] = []
    fid = itertools.count()
    for n, c in enumerate(rle):
        ic = int(c)
        # Odd-numbered elements = empty space
        if n % 2:
            disk.extend([None] * ic)
        else:
            disk.extend([next(fid)] * ic)
    return disk


def compact_disk_image(image: list[int | None]):
    empty_locs = deque(
        n
        for n, fid in enumerate(image)
        if fid is None
    )
    new_image = image.copy()
    while empty_locs:
        fid = new_image.pop()
        src_loc = len(new_image)
        if fid is None:
            empty_locs.remove(src_loc)
            continue
        dst_loc = empty_locs.popleft()
        new_image[dst_loc] = fid
    return new_image


def defrag_disk_image(image: list[int | None]):
    file_spans: dict[int, tuple[int, int]] = {}
    empty_spans: list[tuple[int, int]] = []
    _start = 0
    _count = 1
    _prev_fid = image[0]
    for i, fid in enumerate(image[1:], start=1):
        if fid == _prev_fid:
            _count += 1
            continue
        if _prev_fid is not None:
            file_spans[_prev_fid] = (_start, _count)
        else:
            empty_spans.append((_start, _count))
        _prev_fid = fid
        _start = i
        _count = 1
    if _prev_fid is not None:
        file_spans[_prev_fid] = (_start, _count)
    else:
        empty_spans.append((_start, _count))

    new_file_spans: dict[int, tuple[int, int]] = {}
    for fid, (_start, _count) in reversed(file_spans.items()):
        for i, (_est, _eco) in enumerate(empty_spans):
            if _est == -1:
                continue
            if _est > _start:
                new_file_spans[fid] = _start, _count
                break
            if _eco < _count:
                continue
            new_file_spans[fid] = (_est, _count)
            if (new_eco := _eco - _count) == 0:
                empty_spans[i] = (-1, -1)
            else:
                new_est = _est + _count
                empty_spans[i] = (new_est, new_eco)
            break
        else:
            # We do not find any space for moving the file
            new_file_spans[fid] = _start, _count

    new_image: list[int | None] = [None] * len(image)
    for fid, (_start, _count) in new_file_spans.items():
        for i in range(_start, _start + _count):
            new_image[i] = fid
    return new_image


def checksum(image: list[int | None]) -> int:
    return sum(
        n * fid
        for n, fid in enumerate(image)
        if fid is not None
    )


def _test():
    with io.StringIO(TEST_VECTOR) as fin:
        rle = consume(fin)

    image1 = build_disk_image(rle)
    image2 = compact_disk_image(image1)
    result = checksum(image2)
    print("Test 1:", result)
    assert result == TEST_EXPECT_1

    image1 = build_disk_image(rle)
    image2 = defrag_disk_image(image1)
    result = checksum(image2)
    print("Test 2:", result)
    assert result == TEST_EXPECT_2


def _main():
    data_file = Path(sys.argv[0]).with_suffix(".txt")
    with open(data_file, "rt") as fin:
        rle = consume(fin)

    image1 = build_disk_image(rle)
    image2 = compact_disk_image(image1)
    result = checksum(image2)
    print("Case 1:", result)

    image1 = build_disk_image(rle)
    image2 = defrag_disk_image(image1)
    result = checksum(image2)
    print("Case 2:", result)


if __name__ == '__main__':
    _test()
    _main()
