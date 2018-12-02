#!/usr/bin/env python
from __future__ import print_function

INPUT_FILE_PATH = 'day1-input.txt'
def read_input():
    with open(INPUT_FILE_PATH) as f:
        return f.readlines()


def parse_delta(delta):
    return int(delta)


def apply_delta(curr, delta):
    return curr + delta


def main_part1():
    freq = 0

    deltas = read_input()

    for delta in deltas:
        freq = apply_delta(freq, parse_delta(delta))

    print("Part 1 result: " + str(freq))


def main_part2():
    freq = 0
    seen_freqs = {}

    deltas = read_input()
    delta_idx = 0
    while True:
        delta = parse_delta(deltas[delta_idx])
        freq = apply_delta(freq, delta)

        if freq in seen_freqs:
            break
        else:
            # the value doesn't matter though, we're using the dict as a set
            seen_freqs[freq] = 1

        delta_idx += 1
        if delta_idx >= len(deltas):
            delta_idx = 0

    print("Part 2 result: " + str(freq))


if __name__ == '__main__':
    main_part1()
    main_part2()
