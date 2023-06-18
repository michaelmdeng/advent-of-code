# pylint: disable=invalid-name
from enum import Enum
from functools import reduce
from unittest import TestCase

from shared import AdventDay, AdventDayRunner


class Day3(AdventDay):
    class WireDirection(Enum):
        LEFT = "L"
        RIGHT = "R"
        UP = "U"
        DOWN = "D"

    class WireOrientation(Enum):
        VERTICAL = 0
        HORIZONTAL = 1

        @staticmethod
        def of(direction):
            if direction in (Day3.WireDirection.LEFT, Day3.WireDirection.RIGHT):
                return Day3.WireOrientation.HORIZONTAL
            elif direction in (Day3.WireDirection.UP, Day3.WireDirection.DOWN):
                return Day3.WireOrientation.VERTICAL
            else:
                raise ValueError(f"Invalid direction: {direction}.")

    class WireSegment:
        def __init__(self, x, y, end_x, end_y):
            self.x = x
            self.y = y
            self.end_x = end_x
            self.end_y = end_y

            self.l = Day3.distance(self.x, self.y, self.end_x, self.end_y)

        @property
        def min_x(self):
            return min(self.x, self.end_x)

        @property
        def max_x(self):
            return max(self.x, self.end_x)

        @property
        def min_y(self):
            return min(self.y, self.end_y)

        @property
        def max_y(self):
            return max(self.y, self.end_y)

        def intersections(self, segment):
            x_overlap = (
                segment.min_x <= self.max_x and segment.min_x >= self.min_x
            ) or (self.min_x <= segment.max_x and self.min_x >= segment.min_x)
            y_overlap = (
                segment.min_y <= self.max_y and segment.min_y >= self.min_y
            ) or (self.min_y <= segment.max_y and self.min_y >= segment.min_y)

            if x_overlap and y_overlap:
                x_range = range(
                    max(self.min_x, segment.min_x), min(self.max_x, segment.max_x) + 1
                )
                y_range = range(
                    max(self.min_y, segment.min_y), min(self.max_y, segment.max_y) + 1
                )

                return [(x, y) for x in x_range for y in y_range]
            else:
                return []

    @staticmethod
    def distance(x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    @staticmethod
    def segment(x, y, l, direction):
        if Day3.WireOrientation.of(direction) == Day3.WireOrientation.VERTICAL:
            end_x = x

            if direction == Day3.WireDirection.DOWN:
                end_y = y - l
            else:
                end_y = y + l
        else:
            end_y = y

            if direction == Day3.WireDirection.LEFT:
                end_x = x - l
            else:
                end_x = x + l

        return Day3.WireSegment(x, y, end_x, end_y)

    @staticmethod
    def segments(steps):
        x = 0
        y = 0

        out = []
        for step in steps:
            direction = Day3.WireDirection(step[0])
            l = int(step[1:])

            segment = Day3.segment(x, y, l, direction)
            out.append(segment)

            x = segment.end_x
            y = segment.end_y

        return out

    @staticmethod
    def min_distance(segments1, segments2):
        intersections = reduce(
            lambda l1, l2: l1 + l2,
            [
                segment1.intersections(segment2)
                for segment1 in segments1
                for segment2 in segments2
            ],
        )

        # remove starting point as intersection
        intersections = [pt for pt in intersections if pt[0] != 0 or pt[1] != 0]

        return min(
            [
                Day3.distance(intersection[0], intersection[1], 0, 0)
                for intersection in intersections
            ]
        )

    @staticmethod
    def min_travel(segments1, segments2):
        travels = []
        travel1 = 0
        for segment1 in segments1:
            travel2 = 0
            for segment2 in segments2:
                for intersection in segment1.intersections(segment2):
                    if intersection[0] == 0 and intersection[1] == 0:
                        continue

                    distance1 = Day3.distance(
                        intersection[0], intersection[1], segment1.x, segment1.y
                    )
                    distance2 = Day3.distance(
                        intersection[0], intersection[1], segment2.x, segment2.y
                    )

                    travels.append(travel1 + distance1 + travel2 + distance2)

                travel2 = travel2 + segment2.l

            travel1 = travel1 + segment1.l

        return min(travels)

    def __init__(self):
        AdventDay.__init__(self, 2019, 3)

    def part_1(self):
        paths = self.input_data
        steps1 = paths[0].split(",")
        steps2 = paths[1].split(",")

        segments1 = Day3.segments(steps1)
        segments2 = Day3.segments(steps2)

        return Day3.min_distance(segments1, segments2)

    def part_2(self):
        paths = self.input_data
        steps1 = paths[0].split(",")
        steps2 = paths[1].split(",")

        segments1 = Day3.segments(steps1)
        segments2 = Day3.segments(steps2)

        return Day3.min_travel(segments1, segments2)


class Day3Tests(AdventDayRunner, TestCase):
    instance_cls = Day3

    def test_part_1_example(self):
        example_steps1 = [
            "R8,U5,L5,D3",
            "R75,D30,R83,U83,L12,D49,R71,U7,L72",
            "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
        ]
        example_steps1 = [steps.split(",") for steps in example_steps1]

        example_steps2 = [
            "U7,R6,D4,L4",
            "U62,R66,U55,R34,D71,R55,D58,R83",
            "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7",
        ]
        example_steps2 = [steps.split(",") for steps in example_steps2]

        example_distances = [6, 159, 135]

        for steps1, steps2, distance in zip(
            example_steps1, example_steps2, example_distances
        ):
            segments1 = Day3.segments(steps1)
            segments2 = Day3.segments(steps2)

            assert Day3.min_distance(segments1, segments2) == distance

    def test_part_2_example(self):
        example_steps1 = [
            "R8,U5,L5,D3",
            "R75,D30,R83,U83,L12,D49,R71,U7,L72",
            "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
        ]
        example_steps1 = [steps.split(",") for steps in example_steps1]

        example_steps2 = [
            "U7,R6,D4,L4",
            "U62,R66,U55,R34,D71,R55,D58,R83",
            "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7",
        ]
        example_steps2 = [steps.split(",") for steps in example_steps2]

        example_travels = [30, 610, 410]

        for steps1, steps2, travel in zip(
            example_steps1, example_steps2, example_travels
        ):
            segments1 = Day3.segments(steps1)
            segments2 = Day3.segments(steps2)

            assert Day3.min_travel(segments1, segments2) == travel
