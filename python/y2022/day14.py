from typing import Optional

from shared import AdventDayV2


class Day14(AdventDayV2):
    def __init__(self):
        super(Day14, self).__init__()

    def fill(
        self, grid: list[list[str]], i_range: tuple[int, int], j_range: tuple[int, int]
    ) -> tuple[bool, Optional[tuple[int, int]]]:
        min_i, max_i = i_range
        min_j, max_j = j_range
        sand_start = (0, 500)
        sand_start_grid = (sand_start[0], sand_start[1] - min_j)

        curr_sand = sand_start_grid
        while True:
            down = (curr_sand[0] + 1, curr_sand[1])
            if (
                down[0] >= len(grid)
                or grid[down[0]][down[1]] == "o"
                or grid[down[0]][down[1]] == "#"
            ):
                pass
            else:
                curr_sand = down
                continue

            left = (curr_sand[0] + 1, curr_sand[1] - 1)
            if (
                left[0] >= len(grid)
                or left[1] < 0
                or grid[left[0]][left[1]] == "o"
                or grid[left[0]][left[1]] == "#"
            ):
                pass
            else:
                curr_sand = left
                continue

            right = (curr_sand[0] + 1, curr_sand[1] + 1)
            if (
                right[0] >= len(grid)
                or right[1] >= len(grid[0])
                or grid[right[0]][right[1]] == "o"
                or grid[right[0]][right[1]] == "#"
            ):
                pass
            else:
                curr_sand = right
                continue

            break

        possible = [down, left, right]
        if (
            all(coord[0] >= 0 for coord in possible)
            and all(coord[0] < len(grid) for coord in possible)
            and all(coord[1] >= 0 for coord in possible)
            and all(coord[1] < len(grid[0]) for coord in possible)
        ):
            grid[curr_sand[0]][curr_sand[1]] = "o"
            return True, curr_sand
        else:
            return False, None

        grid[sand_start_grid[0]][sand_start_grid[1]] = "+"

    def generate_grid(
        self,
        paths: list[list[tuple[int, int]]],
        i_range: tuple[int, int],
        j_range: tuple[int, int],
        set_floor=False,
    ) -> list[list[str]]:
        min_i, max_i = i_range
        min_j, max_j = j_range

        grid = [["." for i in range(min_j, max_j + 1)] for j in range(min_i, max_i + 1)]
        for path in paths:
            for coord_idx in range(len(path) - 1):
                j1, i1 = path[coord_idx]
                j2, i2 = path[coord_idx + 1]

                if j1 == j2:
                    points = [[j1, i] for i in range(min(i1, i2), max(i1, i2) + 1)]
                else:
                    points = [[j, i1] for j in range(min(j1, j2), max(j1, j2) + 1)]

                for point in points:
                    j, i = point
                    row_idx = i - min_i
                    col_idx = j - min_j
                    grid[row_idx][col_idx] = "#"

        if set_floor:
            for j in range(max_j - min_j + 1):
                grid[max_i][j] = "#"

        return grid

    def parse_paths(self, input: list[str]) -> list[list[tuple[int, int]]]:
        paths = []
        for line in input:
            path = []
            for part in line.strip().split("->"):
                coord = part.split(",")
                path.append((int(coord[0]), int(coord[1])))
            paths.append(path)

        return paths

    def run_part_1(self, input) -> int:
        paths = self.parse_paths(input)

        min_j = min(coord[0] for path in paths for coord in path)
        min_j = min([min_j, 500])
        max_j = max(coord[0] for path in paths for coord in path)
        max_j = max([max_j, 500])
        min_i = min(coord[1] for path in paths for coord in path)
        min_i = min([min_i, 0])
        max_i = max(coord[1] for path in paths for coord in path)

        grid = self.generate_grid(paths, (min_i, max_i), (min_j, max_j))

        fill_count = 0
        while True:
            filled, _ = self.fill(grid, (min_i, max_i), (min_j, max_j))
            if not filled:
                break
            else:
                fill_count += 1

        return fill_count

    def run_part_2(self, input) -> int:
        paths = self.parse_paths(input)

        min_i = min(coord[1] for path in paths for coord in path)
        min_i = min([min_i, 0])
        max_i = max(coord[1] for path in paths for coord in path)
        max_i = max_i + 2
        min_j = min(coord[0] for path in paths for coord in path)
        min_j = min([min_j, 500 - max_i - 1])
        max_j = max(coord[0] for path in paths for coord in path)
        max_j = max([max_j, 500 + max_i + 1])

        grid = self.generate_grid(paths, (min_i, max_i), (min_j, max_j), set_floor=True)

        fill_count = 0
        fill_coord = None
        while fill_coord != (0, 500 - min_j):
            filled, fill_coord = self.fill(grid, (min_i, max_i), (min_j, max_j))
            if not filled:
                break
            else:
                fill_count += 1

        return fill_count


class Day14Tests(AdventDayV2.Tests):
    instance_cls = Day14
    EXPECTED = {
        (1, True): 24,
        (1, False): 672,
        (2, True): 93,
        (2, False): 26831,
    }
