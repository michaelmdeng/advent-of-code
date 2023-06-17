from unittest import TestCase

from shared import AdventDay, AdventDayRunner

class Day8(AdventDay):
    def __init__(self):
        AdventDay.__init__(self, 2022, 8)

    def part_1(self):
        input = self.input_data

        tree_grid = []
        for line in input:
            tree_grid.append(line.strip())

        top_visible = []
        bottom_visible = []
        left_visible = []
        right_visible = []
        for row in tree_grid:
            top_visible.append([False for c in row])
            bottom_visible.append([False for c in row])
            left_visible.append([False for c in row])
            right_visible.append([False for c in row])

        for row_idx, row in enumerate(tree_grid):
            for col_idx, tree_height in enumerate(row):
                above_row_idx = range(0, row_idx)
                above_heights = [tree_grid[ridx][col_idx] for ridx in above_row_idx]

                if len(above_heights) == 0 or all([height < tree_height for height in above_heights]):
                    top_visible[row_idx][col_idx] = True

                below_row_idx = range(row_idx + 1, len(tree_grid))
                below_heights = [tree_grid[ridx][col_idx] for ridx in below_row_idx]

                if len(below_heights) == 0 or all([height < tree_height for height in below_heights]):
                    bottom_visible[row_idx][col_idx] = True

                to_left_col_idx = range(0, col_idx)
                to_left_heights = [tree_grid[row_idx][cidx] for cidx in to_left_col_idx]
                if len(to_left_heights) == 0 or all([height < tree_height for height in to_left_heights]):
                    left_visible[row_idx][col_idx] = True

                to_right_col_idx = range(col_idx + 1, len(tree_grid[0]))
                to_right_heights = [tree_grid[row_idx][cidx] for cidx in to_right_col_idx]
                if len(to_right_heights) == 0 or all([height < tree_height for height in to_right_heights]):
                    right_visible[row_idx][col_idx] = True

        visible = []
        for row in tree_grid:
            visible.append([False for c in row])

        for row_idx in range(0, len(tree_grid)):
            for col_idx in range(0, len(tree_grid[0])):
                visible[row_idx][col_idx] = top_visible[row_idx][col_idx] or bottom_visible[row_idx][col_idx] or left_visible[row_idx][col_idx] or right_visible[row_idx][col_idx]

        total_visible = 0
        for row in visible:
            total_visible += sum([1 for is_visible in row if is_visible])

        return total_visible

    def part_2(self):
        input = self.input_data

        tree_grid = []
        for line in input:
            tree_grid.append([int(c) for c in list(line.strip())])

        scores = [[0 for h in row] for row in tree_grid]
        for row_idx in range(1, len(tree_grid) - 1):
            for col_idx in range(1, len(tree_grid[0]) - 1):
                scores[row_idx][col_idx] = self.scenic_score(row_idx, col_idx, tree_grid)

        return max([max(row) for row in scores])

    def scenic_score(self, row_idx, col_idx, tree_grid):
        curr_height = tree_grid[row_idx][col_idx]
        above = [tree_grid[r][col_idx] for r in range(row_idx - 1, -1, -1)]
        below = [tree_grid[r][col_idx] for r in range(row_idx + 1, len(tree_grid))]
        left = tree_grid[row_idx][col_idx - 1::-1]
        right = tree_grid[row_idx][col_idx + 1:]

        seen_above_idx = next((i for i, h in enumerate(above) if h >= curr_height), -1)
        if seen_above_idx == -1:
            seen_above_idx = len(above) - 1
        seen_above = seen_above_idx + 1

        seen_below_idx = next((i for i, h in enumerate(below) if h >= curr_height), -1)
        if seen_below_idx == -1:
            seen_below_idx = len(below) - 1
        seen_below = seen_below_idx + 1

        seen_left_idx = next((i for i, h in enumerate(left) if h >= curr_height), -1)
        if seen_left_idx == -1:
            seen_left_idx = len(left) - 1
        seen_left = seen_left_idx + 1

        seen_right_idx = next((i for i, h in enumerate(right) if h >= curr_height), -1)
        if seen_right_idx == -1:
            seen_right_idx = len(right) - 1
        seen_right = seen_right_idx + 1

        return seen_above * seen_below * seen_left * seen_right


class Day8Tests(AdventDayRunner, TestCase):
    instance_cls = Day8
