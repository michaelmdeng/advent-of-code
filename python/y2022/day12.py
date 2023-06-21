from collections import deque
from typing import Union
from unittest import TestCase

from shared import AdventDay, AdventDayRunner


class Day12(AdventDay):
    def __init__(self):
        AdventDay.__init__(self, 2022, 12)

    def parse_input(
        self, input: list[str]
    ) -> tuple[list[list[int]], tuple[tuple[int, int], tuple[int, int]]]:
        grid = []
        for row_idx, line in enumerate(input):
            row = []
            for col_idx, c in enumerate(line.strip()):
                if c == "S":
                    start = (row_idx, col_idx)
                    height = 0
                elif c == "E":
                    end = (row_idx, col_idx)
                    height = 25
                else:
                    height = ord(c) - ord("a")

                row.append(height)

            grid.append(row)

        return (grid, (start, end))

    def min_steps(
        self, start: tuple[int, int], end: tuple[int, int], grid: list[list[int]]
    ) -> Union[int, None]:
        num_rows = len(grid)
        num_cols = len(grid[0])
        searched = {}
        searched_grid = [[0 for i in row] for row in grid]

        to_search = [start]
        steps = 0
        while to_search:
            next = []
            for curr in to_search:
                if curr == end:
                    return steps

                if curr in searched:
                    continue

                searched[curr] = steps
                searched_grid[curr[0]][curr[1]] = steps

                curr_height = grid[curr[0]][curr[1]]
                poss_next = [
                    (curr[0] - 1, curr[1]),
                    (curr[0] + 1, curr[1]),
                    (curr[0], curr[1] - 1),
                    (curr[0], curr[1] + 1),
                ]
                poss_next = [
                    (i, j)
                    for i, j in poss_next
                    if i >= 0 and i < num_rows and j >= 0 and j < num_cols
                ]
                poss_next = [(i, j) for i, j in poss_next if (i, j) not in searched]
                poss_next = [
                    (i, j) for i, j in poss_next if (grid[i][j] - curr_height) <= 1
                ]
                next += poss_next

            steps += 1
            to_search = next

        return None

    def run_part_1(self, input) -> int:
        grid, (start, end) = self.parse_input(input)
        steps = self.min_steps(start, end, grid)
        if steps:
            return steps
        else:
            return -1

    def run_part_2(self, input) -> int:
        grid, (start, end) = self.parse_input(input)
        poss_starts = []
        for row_idx, row in enumerate(grid):
            for col_idx, height in enumerate(row):
                if height == 0:
                    poss_starts.append((row_idx, col_idx))

        min_steps = len(grid) * len(grid[0])
        for poss_start in poss_starts:
            poss_min_steps = self.min_steps(poss_start, end, grid)
            if poss_min_steps and poss_min_steps < min_steps:
                min_steps = poss_min_steps

        return min_steps


class Day12Tests(AdventDayRunner, TestCase):
    instance_cls = Day12
