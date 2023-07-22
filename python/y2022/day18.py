from collections import deque
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

    def surface_area(self, points: list[Point3]) -> int:
        point_dict = {p: True for p in points}
        point_adjacents = [0] * len(points)
        for i, point in enumerate(points):
            adjacent = [
                (-1, 0, 0),
                (1, 0, 0),
                (0, -1, 0),
                (0, 1, 0),
                (0, 0, -1),
                (0, 0, 1),
            ]
            for dx, dy, dz in adjacent:
                adj_point = Point3(point.x + dx, point.y + dy, point.z + dz)
                if adj_point in point_dict:
                    point_adjacents[i] += 1

        return sum(6 - adj for adj in point_adjacents)

    def surface_area_brute_force(self, points: list[Point3]) -> int:
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

    def run_part_1(self, input) -> int:
        points = self.parse_part_1(input)
        return self.surface_area(points)

    def run_part_2(self, input) -> int:
        points = self.parse_part_1(input)
        min_x, max_x = min(p.x for p in points), max(p.x for p in points)
        min_y, max_y = min(p.y for p in points), max(p.y for p in points)
        min_z, max_z = min(p.z for p in points), max(p.z for p in points)
        # Widen bounding volume to ensure that the edge of the volume is guaranteed to
        # not be a point in the droplet
        # Additionally, this enables us to search from only a single exterior point and
        # guarantees it can reach all other exterior points
        min_x -= 1
        max_x += 1
        min_y -= 1
        max_y += 1
        min_z -= 1
        max_z += 1

        points_dict = {p: True for p in points}
        outer = {}
        search_que = deque([Point3(min_x, min_y, min_z)])
        while search_que:
            point = search_que.popleft()
            if point in points_dict or point in outer:
                continue
            outer[point] = True

            adjacent = [
                (-1, 0, 0),
                (1, 0, 0),
                (0, -1, 0),
                (0, 1, 0),
                (0, 0, -1),
                (0, 0, 1),
            ]
            for dx, dy, dz in adjacent:
                adj_point = Point3(point.x + dx, point.y + dy, point.z + dz)
                if (
                    adj_point.x >= min_x
                    and adj_point.x <= max_x
                    and adj_point.y >= min_y
                    and adj_point.y <= max_y
                    and adj_point.z >= min_z
                    and adj_point.z <= max_z
                ):
                    search_que.append(adj_point)

        inner_points = []
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                for z in range(min_z, max_z + 1):
                    point = Point3(x, y, z)
                    if point not in points_dict and point not in outer:
                        inner_points.append(point)

        points = points + inner_points
        return self.surface_area(points)


class Day18Tests(AdventDayRunner, TestCase):
    instance_cls = Day18
