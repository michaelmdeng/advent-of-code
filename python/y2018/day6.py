import re
from unittest import TestCase

import shared


def parse_coord(line):
    x = int(re.compile("^.*(?=,)").search(line).group())
    y = int(re.compile("(?<=,\s).*$").search(line).group())
    return (x, y)


def dist(coord1, coord2):
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])


def grid(coords, width):
    def get_points(min_x, max_x, min_y, max_y):
        xs = range(min_x, max_x + 1)
        ys = range(min_y, max_y + 1)
        points = []
        for x in xs:
            for y in ys:
                points.append((x, y))
        return points

    min_x = min([coord[0] for coord in coords])
    max_x = max([coord[0] for coord in coords])
    min_y = min([coord[1] for coord in coords])
    max_y = max([coord[1] for coord in coords])
    return get_points(min_x - width, max_x + width, min_y - width, max_y + width)


def areas(coords, width):
    points = grid(coords, width)

    coord_areas = {}
    for point in points:
        dists = [dist(point, coord) for coord in coords]
        sort_dists = sorted(dists)

        if sort_dists[0] == sort_dists[1]:
            continue

        min_idx = shared.min_idx(dists)
        if min_idx not in coord_areas:
            coord_areas[min_idx] = 0
        coord_areas[min_idx] += 1

    return coord_areas


def total_dist(coord, coords):
    return sum([dist(coord, other_coord) for other_coord in coords])


def min_area(coords):
    points = grid(coords, 0)

    dists = [total_dist(point, coords) for point in points]
    return len([1 for dist in dists if dist < 10000])


def main_1():
    lines = shared.read_input("day6-input.txt")
    coords = [parse_coord(line) for line in lines]

    a = {}
    a1 = areas(coords, 1)
    a2 = areas(coords, 2)
    for key in a1:
        if a1[key] == a2[key]:
            a[key] = a1[key]

    print("Result 1: " + str(max(a.values())))


def main_2():
    lines = shared.read_input("day6-input.txt")
    coords = [parse_coord(line) for line in lines]

    area = min_area(coords)
    print("Result 2: " + str(area))


class Day6Tests(TestCase):
    def setUp(self):
        pass

    def test_part_1(self):
        main_1()

    def test_part_2(self):
        main_2()
