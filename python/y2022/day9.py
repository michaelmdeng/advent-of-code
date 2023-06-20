from collections import namedtuple
from unittest import TestCase

from shared import AdventDay, AdventDayRunner


Point = namedtuple("Point", ["x", "y"])
Motion = namedtuple("Motion", ["direction", "magnitude"])


class Day9(AdventDay):
    def __init__(self):
        AdventDay.__init__(self, 2022, 9)

    def move(self, head: Point, direction) -> Point:
        if direction == "L":
            return Point(head.x - 1, head.y)
        elif direction == "R":
            return Point(head.x + 1, head.y)
        elif direction == "U":
            return Point(head.x, head.y + 1)
        elif direction == "D":
            return Point(head.x, head.y - 1)

    def adjacent(self, point1: Point, point2: Point) -> bool:
        return abs(point1.x - point2.x) <= 1 and abs(point1.y - point2.y) <= 1

    def follow(self, head: Point, tail: Point) -> Point:
        if self.adjacent(head, tail):
            return tail

        new_x = tail.x
        if head.x > tail.x:
            new_x += 1
        elif head.x < tail.x:
            new_x -= 1

        new_y = tail.y
        if head.y > tail.y:
            new_y += 1
        elif head.y < tail.y:
            new_y -= 1

        return Point(new_x, new_y)

    def run_part_1(self, input):
        motions = []
        for line in input:
            dir, mag = line.strip().split()
            motions.append(Motion(direction=dir, magnitude=int(mag)))

        head = Point(0, 0)
        tail = Point(0, 0)
        visited = {}
        for motion in motions:
            for step in range(motion.magnitude):
                head = self.move(head, motion.direction)
                tail = self.follow(head, tail)
                visited[tail] = True

        return len(visited)

    def run_part_2(self, input):
        motions = []
        for line in input:
            dir, mag = line.strip().split()
            motions.append(Motion(direction=dir, magnitude=int(mag)))

        head = Point(0, 0)
        num_tails = 9
        tails = [Point(0, 0) for i in range(num_tails)]
        visited = {}
        for motion in motions:
            for step in range(motion.magnitude):
                head = self.move(head, motion.direction)
                to_follow = head
                for i, tail in enumerate(tails):
                    tail = self.follow(to_follow, tail)
                    tails[i] = tail
                    to_follow = tail

                visited[tails[-1]] = True

        return len(visited)


class Day9Tests(AdventDayRunner, TestCase):
    instance_cls = Day9
