from adventofcode.utils import AbstractSolution
from math import sqrt


def move_tail(head, tail):
    x, y = head
    x_t, y_t = tail
    dx = x - x_t
    dy = y - y_t
    distance = sqrt((x_t - x) ** 2 + (y_t - y) ** 2)
    if distance < 1.5:  # They are close enough to not move
        pass
    else:
        if dx != 0:
            x_t += dx / abs(dx)
        if dy != 0:
            y_t += dy / abs(dy)
    new_tail = (x_t, y_t)
    return new_tail


class Solution(AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        self.puzzle_input = puzzle_input
        self.moves = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}

        position_head = [(0, 0)]
        self.position_tails = [[(0, 0)] for _ in range(9)]

        for line in self.puzzle_input:
            direction, distance = line[0], int(line[1:])
            for step in range(distance):
                new_head = (position_head[-1][0] + self.moves[direction][0], position_head[-1][1] + self.moves[direction][1])
                position_head.append(new_head)
                for knot in range(9):
                    head_of_knot = self.position_tails[knot - 1][-1] if knot > 0 else position_head[-1]
                    new_tail = move_tail(
                        head_of_knot, self.position_tails[knot][-1]
                    )

                    self.position_tails[knot].append(new_tail)

    def part1(self) -> str:
        number_of_unique_positions = len(set(self.position_tails[0]))
        return f"The tail has {number_of_unique_positions} unique positions."

    def part2(self) -> str:
        number_of_unique_positions = len(set(self.position_tails[-1]))
        return f"The tail of the ten knot rope has {number_of_unique_positions} unique positions."
