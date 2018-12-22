#!/usr/bin/env python
from __future__ import print_function
from shared import read_input
import operator
import re

INPUT_FILE_PATH = 'day4-input.txt'


def parse_time(line):
    time_part = re.compile('(?<=^\[).*(?=\])').search(line).group()
    return [int(x) for x in re.split('-| |:|\[|]', time_part)]


def parse_log(line):
    return re.compile('(?<=\]\s).*$').search(line).group()


def parse_id(line):
    return int(re.compile('(?<=#)\d+').search(line).group())


def has_id(line):
    return True if re.compile('(?<=#)\d+').search(line) else False


def main():
    lines = read_input(INPUT_FILE_PATH)

    guard_mins = {}
    guard_times = {}

    curr_id = -1
    start_time = None
    for line in lines:
        if has_id(line):
            curr_id = parse_id(line)

        if 'asleep' in parse_log(line):
            start_time = (parse_time(line)[3], parse_time(line)[4])

        if 'wakes' in parse_log(line):
            end_time = (parse_time(line)[3], parse_time(line)[4])
            if curr_id not in guard_mins:
                guard_mins[curr_id] = 0
                guard_times[curr_id] = {}

            if start_time[0] == 23 or start_time[0] == 1 or end_time[0] == 23 or end_time[0] == 1:
                print('Unexpected')
            else:
                guard_mins[curr_id] += end_time[1] - start_time[1]
                for minute in range(start_time[1], end_time[1]):
                    if minute not in guard_times[curr_id]:
                        guard_times[curr_id][minute] = 0

                    guard_times[curr_id][minute] += 1

    max_id = max(guard_mins.iteritems(), key=operator.itemgetter(1))[0]
    max_min = max(guard_times[max_id].iteritems(),
                  key=operator.itemgetter(1))[0]
    print("Part 1: " + str(max_id * max_min))

    max_id_min = [(curr_id,) + max(guard_times[curr_id].iteritems(),
                                   key=operator.itemgetter(1)) for curr_id in guard_times.keys()]
    max_id = max(max_id_min, key=operator.itemgetter(2))[0]
    max_min = max(max_id_min, key=operator.itemgetter(2))[1]
    print("Part 2: " + str(max_id * max_min))


if __name__ == '__main__':
    main()
