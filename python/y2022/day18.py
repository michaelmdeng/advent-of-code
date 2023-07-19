from collections import namedtuple
from unittest import TestCase

from shared import AdventDay, AdventDayRunner

Point3 = namedtuple("Point3", ["x", "y", "z"])


class Day18(AdventDay):
    def __init__(self):
        AdventDay.__init__(self, 2022, 18)

    def parse_part_1(self, input) -> list[Point3]:
        points = []
        for line in input:
            x, y, z = line.strip().split(",")
            point = Point3(int(x), int(y), int(z))
            points.append(point)

        return points

    def run_part_1(self, input) -> int:
        points = self.parse_part_1(input)

        point_adjacents = []
        for i, point1 in enumerate(points):
            adjacent = 0
            for j, point2 in enumerate(points):
                if i == j:
                    continue

                if (
                    abs(point1.x - point2.x)
                    + abs(point1.y - point2.y)
                    + abs(point1.z - point2.z)
                    <= 1
                ):
                    adjacent += 1

            point_adjacents.append(adjacent)

        return sum(6 - adj for adj in point_adjacents)

    def run_part_2(self, input) -> None:
        pass


class Day18Tests(AdventDayRunner, TestCase):
    instance_cls = Day18
