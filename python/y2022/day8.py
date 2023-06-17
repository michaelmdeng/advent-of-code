from unittest import TestCase

from shared import AdventDay, AdventDayRunner

class Day8(AdventDay):
    def __init__(self):
        AdventDay.__init__(self, 2022, 8)

    def part_1(self):
        input = self.input_data
        # input = [
        #     '30373',
        #     '25512',
        #     '65332',
        #     '33549',
        #     '35390'
        # ]

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


        # print(tree_grid)
        # print(top_visible)
        # print(bottom_visible)
        # print(left_visible)
        # print(right_visible)

        visible = []
        for row in tree_grid:
            visible.append([False for c in row])

        for row_idx in range(0, len(tree_grid)):
            for col_idx in range(0, len(tree_grid[0])):
                visible[row_idx][col_idx] = top_visible[row_idx][col_idx] or bottom_visible[row_idx][col_idx] or left_visible[row_idx][col_idx] or right_visible[row_idx][col_idx]

        # print(visible)

        total_visible = 0
        for row in visible:
            total_visible += sum([1 for is_visible in row if is_visible])

        return total_visible

    def part_2(self):
        pass


class Day8Tests(AdventDayRunner, TestCase):
    instance_cls = Day8
