from adventofcode.utils import AbstractSolution


def compute_scenic_score(grid, row, col):
    val = int(grid[row][col])
    visibility_left = 0
    for i in range(1, col + 1):
        visibility_left += 1
        if val <= int(grid[row][col - i]):
            break
    visibility_right = 0
    for i in range(1, len(grid[0]) - col):
        visibility_right += 1
        if val <= int(grid[row][col + i]):
            break
    visibility_top = 0
    for i in range(1, row + 1):
        visibility_top += 1
        if val <= int(grid[row - i][col]):
            break
    visibility_bottom = 0
    for i in range(1, len(grid) - row):
        visibility_bottom += 1
        if val <= int(grid[row + i][col]):
            break
    return visibility_left * visibility_right * visibility_top * visibility_bottom


def check_visibility_left(grid, row, col, val):
    if col == 0:
        return True
    if check_visibility_left(grid, row, col - 1, val) and val > int(grid[row][col - 1]):
        return True
    return False


def check_visibility_right(grid, row, col, val):
    if col == len(grid[0]) - 1:
        return True
    if check_visibility_right(grid, row, col + 1, val) and val > int(grid[row][col + 1]):
        return True
    return False


def check_visibility_top(grid, row, col, val):
    if row == 0:
        return True
    if check_visibility_top(grid, row - 1, col, val) and val > int(grid[row - 1][col]):
        return True
    return False


def check_visibility_bottom(grid, row, col, val):
    if row == len(grid) - 1:
        return True
    if check_visibility_bottom(grid, row + 1, col, val) and val > int(grid[row + 1][col]):
        return True
    return False


def check_visibility(grid, row, col):
    val = int(grid[row][col])
    return 1 if (
            check_visibility_left(grid, row, col, val)
            or check_visibility_right(grid, row, col, val)
            or check_visibility_top(grid, row, col, val)
            or check_visibility_bottom(grid, row, col, val)
    ) else 0


class Solution(AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        self.forest = puzzle_input
        self.visibility = [[check_visibility(self.forest, i, j) for j in range(len(self.forest[0]))] for i in range(len(self.forest))]

    def part1(self) -> str:
        return f"The sum of all visible trees is {sum([sum(row) for row in self.visibility])}"

    def part2(self) -> str:
        scenic_grid = [[compute_scenic_score(self.forest, i, j) for j in range(len(self.forest[0]))] for i in range(len(self.forest))]
        return f"The maximum of the scenic grid is {max([max(row) for row in scenic_grid])}"
