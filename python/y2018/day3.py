import re
from unittest import TestCase

from shared import read_input


INPUT_FILE_PATH = 'day3-input.txt'


class Rectangle:
    def __init__(self, x_off, y_off, x_wid, y_wid):
        assert(x_off >= 0)
        assert(y_off >= 0)
        assert(x_wid >= 0)
        assert(y_wid >= 0)
        self.x_off = x_off
        self.y_off = y_off
        self.x_wid = x_wid
        self.y_wid = y_wid

    def intersect(self, other):
        min_x = self.x_off
        max_x = self.x_off + self.x_wid - 1
        min_y = self.y_off
        max_y = self.y_off + self.y_wid - 1
        min_x_oth = other.x_off
        max_x_oth = other.x_off + other.x_wid - 1
        min_y_oth = other.y_off
        max_y_oth = other.y_off + other.y_wid - 1

        return (max_x_oth >= min_x and max_x >= min_x_oth and
                max_y_oth >= min_y and max_y >= min_y_oth)

    def __str__(self):
        return 'Rect({}, {}, {}, {})'.format(self.x_off, self.y_off, self.x_wid, self.y_wid)


def parse_claim(claim):
    claim_id = int(re.compile('(?<=^#)\d+').search(claim).group())
    x_off = int(re.compile('(?<=@\s)\d+').search(claim).group())
    y_off = int(re.compile('(?<=,)\d+(?=:)').search(claim).group())
    x_wid = int(re.compile('(?<=:\s)\d+(?=x)').search(claim).group())
    y_wid = int(re.compile('(?<=x)\d+(?=$)').search(claim).group())

    return (claim_id, Rectangle(x_off, y_off, x_wid, y_wid))


def main_1():
    claims_str = read_input(INPUT_FILE_PATH)
    claims = [parse_claim(claim_str) for claim_str in claims_str]

    overlap = {}
    for claim in claims:
        xs = range(claim[1].x_off, claim[1].x_off + claim[1].x_wid)
        ys = range(claim[1].y_off, claim[1].y_off + claim[1].y_wid)
        for x in xs:
            for y in ys:
                if not (x, y) in overlap:
                    overlap[(x, y)] = False
                else:
                    overlap[(x, y)] = True

    print(len([x for x in overlap.keys() if overlap[x]]))


def main_2():
    claims_str = read_input(INPUT_FILE_PATH)
    claims = [parse_claim(claim_str) for claim_str in claims_str]

    for idx in range(0, len(claims)):
        intersect_any = False
        for idx_oth in range(0, len(claims)):
            if idx == idx_oth:
                continue

            if claims[idx][1].intersect(claims[idx_oth][1]):
                intersect_any = True
                break

        if not intersect_any:
            print(claims[idx][0])


class Day3Tests(TestCase):
    def setUp(self):
        pass

    def test_part_1(self):
        main_1()

    def test_part_2(self):
        main_2()
