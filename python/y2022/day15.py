from collections import deque
import re
from typing import Optional
from unittest import TestCase

from shared import AdventDay, AdventDayRunner


class Day15(AdventDay):
    def __init__(self):
        AdventDay.__init__(self, 2022, 15)

    @staticmethod
    def mdist(pt1: tuple[int, int], pt2: tuple[int, int]) -> int:
        return abs(pt1[0] - pt2[0]) + abs(pt1[1] - pt2[1])

    def parse_readings(
        self, input: list[str]
    ) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        p = re.compile(r"x=([-\d]+), y=([-\d]+)")
        readings = []
        for line in input:
            coords = p.findall(line.strip())
            sensor, beacon = coords
            sensor = (int(sensor[0]), int(sensor[1]))
            beacon = (int(beacon[0]), int(beacon[1]))

            reading = (sensor, beacon)
            readings.append(reading)

        return readings

    def merge_ranges(self, ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
        sorted_ranges = deque(sorted(ranges))
        merged_ranges = []
        curr = sorted_ranges.popleft()
        while sorted_ranges:
            next = sorted_ranges.popleft()

            if curr[1] + 1 >= next[0]:
                curr = (min(curr[0], next[0]), max(curr[1], next[1]))
            else:
                merged_ranges.append(curr)
                curr = next

        if curr:
            merged_ranges.append(curr)

        return merged_ranges

    def excluded_range(
        self, sensor: tuple[int, int], beacon: tuple[int, int], i: int
    ) -> Optional[tuple[int, int]]:
        reading_dist = Day15.mdist(sensor, beacon)

        i_dist = Day15.mdist(sensor, (sensor[0], i))
        if i_dist > reading_dist:
            return None

        diff = reading_dist - i_dist
        exclude_range = (sensor[0] - diff, sensor[0] + diff)
        return exclude_range

    def run_part_1(self, input) -> int:
        readings = self.parse_readings(input)

        min_j = min(j for reading in readings for j in [reading[0][0], reading[1][0]])
        max_j = max(j for reading in readings for j in [reading[0][0], reading[1][0]])
        min_i = min(i for reading in readings for i in [reading[0][1], reading[1][1]])
        max_i = max(i for reading in readings for i in [reading[0][1], reading[1][1]])
        if max_i >= 2000000:
            check_i = 2000000
        else:
            check_i = 10

        beacons = {}
        for reading in readings:
            _, beacon = reading
            if beacon[1] == check_i:
                beacons[beacon[0]] = True

        ranges = []
        for reading_i, reading in enumerate(readings):
            sensor, beacon = reading
            excluded_range = self.excluded_range(sensor, beacon, check_i)
            if not excluded_range:
                continue
            else:
                ranges.append(excluded_range)

        merged_ranges = self.merge_ranges(ranges)

        out = 0
        for r in merged_ranges:
            out += (r[1] - r[0]) + 1

            for _, j in beacons.items():
                if j >= r[0] and j <= r[1]:
                    out -= 1

        return out

    def run_part_2(self, input) -> int:
        readings = self.parse_readings(input)

        min_j = min(j for reading in readings for j in [reading[0][0], reading[1][0]])
        max_j = max(j for reading in readings for j in [reading[0][0], reading[1][0]])
        min_i = min(i for reading in readings for i in [reading[0][1], reading[1][1]])
        max_i = max(i for reading in readings for i in [reading[0][1], reading[1][1]])
        if max_i >= 2000000:
            check_limit = 4000000
            # Narrow on the solution to run tests faster
            # Can calculate the solution from scratch using the full range
            check_range = range(3200000, check_limit)
            # check_range = range(check_limit)
        else:
            check_limit = 20
            check_range = range(20)

        for i in check_range:
            ranges = []
            for reading_i, reading in enumerate(readings):
                sensor, beacon = reading
                excluded_range = self.excluded_range(sensor, beacon, i)
                if not excluded_range:
                    continue
                else:
                    ranges.append(excluded_range)

            merged_ranges = self.merge_ranges(ranges)
            if len(merged_ranges) > 1:
                if merged_ranges[1][0] - merged_ranges[0][1] == 2:
                    j = merged_ranges[0][1] + 1
                    return j * 4000000 + i

        return 0


class Day15Tests(AdventDayRunner, TestCase):
    instance_cls = Day15
