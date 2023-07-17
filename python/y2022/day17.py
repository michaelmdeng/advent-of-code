from collections import deque
from unittest import TestCase

from shared import AdventDay, AdventDayRunner

#  ####
#
#  .#.
#  ###
#  .#.
#
#  ..#
#  ..#
#  ###
#
#  #
#  #
#  #
#  #
#
#  ##
#  ##
ROCKS = [
    [["#", "#", "#", "#"]],
    [[".", "#", "."], ["#", "#", "#"], [".", "#", "."]],
    [["#", "#", "#"], [".", ".", "#"], [".", ".", "#"]],
    [["#"], ["#"], ["#"], ["#"]],
    [["#", "#"], ["#", "#"]],
]
ROCK_HEIGHTS = {
    0: 1,
    1: 3,
    2: 3,
    3: 4,
    4: 2,
}
ROCK_WIDTHS = {
    0: 4,
    1: 3,
    2: 3,
    3: 1,
    4: 2,
}

Point = tuple[int, int]
Rock = list[list[str]]
RockId = int
Chamber = list[list[str]]


class Day17(AdventDay):
    def __init__(self):
        AdventDay.__init__(self, 2022, 17)

    def parse_part_1(self, input) -> list[str]:
        return list(input[0].strip())

    def get_rock(self, rock_idx: int) -> Rock:
        return ROCKS[rock_idx % len(ROCKS)]

    def chamber(self, rock_positions: list[tuple[Point, RockId]]) -> Chamber:
        height = max(
            [
                pos[0] + len(ROCKS[rock_idx % len(ROCKS)])
                for pos, rock_idx in rock_positions
            ]
        )
        width = 7

        chamber = [["." for _ in range(width)] for _ in range(height)]
        for pos, rock_idx in rock_positions:
            rock = ROCKS[rock_idx % len(ROCKS)]
            for rock_i, rock_row in enumerate(rock):
                for rock_j, rock_char in enumerate(rock_row):
                    chamber[pos[0] + rock_i][pos[1] + rock_j] = rock_char

        chamber.reverse()
        return chamber

    def possible_overlap(
        self, pos1: Point, rock1_idx: int, pos2: Point, rock2_idx: int
    ) -> bool:
        i_overlap = False
        if pos1[0] >= pos2[0] and pos1[0] <= pos2[0] + ROCK_HEIGHTS[rock2_idx] - 1:
            i_overlap = True
        if (
            not i_overlap
            and pos2[0] >= pos1[0]
            and pos2[0] <= pos1[0] + ROCK_HEIGHTS[rock1_idx] - 1
        ):
            i_overlap = True

        j_overlap = False
        if pos1[1] >= pos2[1] and pos1[1] <= pos2[1] + ROCK_WIDTHS[rock2_idx] - 1:
            j_overlap = True
        if (
            not j_overlap
            and pos2[1] >= pos1[1]
            and pos2[1] <= pos1[1] + ROCK_WIDTHS[rock1_idx] - 1
        ):
            j_overlap = True

        return i_overlap and j_overlap

    def overlap(self, pos1: Point, rock1: Rock, pos2: Point, rock2: Rock) -> bool:
        for rock_i, rock_row in enumerate(rock1):
            i = pos1[0] + rock_i
            rock2_i = i - pos2[0]
            for rock_j, char in enumerate(rock_row):
                if char != "#":
                    continue

                j = pos1[1] + rock_j
                rock2_j = j - pos2[1]

                if (
                    rock2_i >= 0
                    and rock2_i < len(rock2)
                    and rock2_j >= 0
                    and rock2_j < len(rock2[0])
                ):
                    if rock2[rock2_i][rock2_j] == "#":
                        return True

        return False

    def simulate(self, jets: list[str], n: int) -> int:
        rock_positions: deque[tuple[Point, RockId]] = deque()
        t = 0
        for rock_ct in range(n):
            # if rock_idx != 0 and rock_idx % 1000 == 0:
            #     print(rock_idx)

            rock_idx = rock_ct % len(ROCKS)
            rock = self.get_rock(rock_idx)
            if rock_positions:
                highest = max([pos[0] + ROCK_HEIGHTS[i] for pos, i in rock_positions])
            else:
                highest = 0

            pos = highest + 3, 2

            move_count = 0
            while True:
                rock_width = len(rock[0])
                rock_height = len(rock)

                # jet movement
                jet = jets[t % len(jets)]
                if jet == "<":
                    next_pos = pos[0], max(0, pos[1] - 1)

                    if move_count <= 3:
                        pos = next_pos
                    else:
                        possible_rocks = [
                            (other_pos, self.get_rock(other_rock_idx))
                            for other_pos, other_rock_idx in rock_positions
                            if self.possible_overlap(
                                next_pos, rock_idx, other_pos, other_rock_idx
                            )
                        ]
                        rock_overlap = any(
                            True
                            for other_pos, other_rock in possible_rocks
                            if self.overlap(next_pos, rock, other_pos, other_rock)
                        )
                        if not rock_overlap:
                            pos = next_pos
                else:  # jet == '>':
                    next_pos = pos[0], min(pos[1] + 1, 7 - rock_width)

                    if move_count <= 3:
                        pos = next_pos
                    else:
                        possible_rocks = [
                            (other_pos, self.get_rock(other_rock_idx))
                            for other_pos, other_rock_idx in rock_positions
                            if self.possible_overlap(
                                next_pos, rock_idx, other_pos, other_rock_idx
                            )
                        ]
                        rock_overlap = any(
                            True
                            for other_pos, other_rock in possible_rocks
                            if self.overlap(next_pos, rock, other_pos, other_rock)
                        )
                        if not rock_overlap:
                            pos = next_pos

                t += 1

                # gravity movement
                next_pos = pos[0] - 1, pos[1]
                if False:
                    pos = next_pos
                else:
                    possible_rocks = [
                        (other_pos, self.get_rock(other_rock_idx))
                        for other_pos, other_rock_idx in rock_positions
                        if self.possible_overlap(
                            next_pos, rock_idx, other_pos, other_rock_idx
                        )
                    ]
                    rock_overlap = any(
                        True
                        for other_pos, other_rock in possible_rocks
                        if self.overlap(next_pos, rock, other_pos, other_rock)
                    )

                    if rock_overlap:
                        break

                if next_pos[0] < 0:
                    pos = 0, pos[1]
                    break

                pos = next_pos
                move_count += 1

            rock_positions.append((pos, rock_idx))
            if len(rock_positions) > 17:
                rock_positions.popleft()

        highest = max([pos[0] + ROCK_HEIGHTS[i] for pos, i in rock_positions])
        return highest

    def run_part_1(self, input) -> int:
        jets = self.parse_part_1(input)
        return self.simulate(jets, 2022)

    def run_part_2(self, input) -> None:
        # TODO
        pass
        # jets = self.parse_part_1(input)
        # jet_count = len(jets)
        # last = None
        # for i in range(1, 20):
        #     curr = self.simulate(jets, jet_count * i)
        #     if last is not None:
        #         print(curr - last)
        #     last = curr
        #     # print(self.simulate(jets, jet_count * i))
        # return self.simulate(jets, 2022)


class Day17Tests(AdventDayRunner, TestCase):
    instance_cls = Day17
