from adventofcode.utils import AbstractSolution, parse_puzzle_input
import numpy as np


class Solution(AbstractSolution):
    def parse(self, puzzle_input: str) -> None:
        self.map = parse_puzzle_input(puzzle_input, block_delimiter='\n', delimiter='', as_array=True).astype(int)
        self.width, self.height = self.map.shape
        self.min_risk_map = np.full(self.map.shape, np.inf)

    def _explore2(self):
        for y in range(self.height - 1, -1, -1):
            for x in range(self.width - 1, -1, -1):
                if x == self.width - 1 and y == self.height - 1:
                    self.min_risk_map[y, x] = self.map[y, x]
                else:
                    options = []
                    if x > 0:
                        options.append(self.min_risk_map[y, x - 1])
                    if x < self.width - 1:
                        options.append(self.min_risk_map[y, x + 1])
                    if y > 0:
                        options.append(self.min_risk_map[y - 1, x])
                    if y < self.height - 1:
                        options.append(self.min_risk_map[y + 1, x])

                    if len(options) > 0:
                        self.min_risk_map[y, x] = self.map[y, x] + min(options)

    def part1(self) -> str:
        min_risk = np.inf
        self._explore2()
        while min_risk != self.min_risk_map[0, 0] - 1:
            min_risk = self.min_risk_map[0, 0] - 1
            self._explore2()

        return f"The minimum risk found is {int(min_risk)}."

    def part2(self) -> str:
        big_map = np.zeros((self.height * 5, self.width * 5), dtype=int)
        for x_offset in range(5):
            for y_offset in range(5):
                for y in range(self.height):
                    for x in range(self.width):
                        big_map[y + y_offset * self.height, x + x_offset * self.width] = (self.map[y, x] + x_offset + y_offset - 1) % 9 + 1
        self.map = big_map
        self.width, self.height = self.map.shape
        self.min_risk_map = np.full(self.map.shape, np.inf)

        min_risk = np.inf
        self._explore2()
        while min_risk != self.min_risk_map[0, 0] - 1:
            min_risk = self.min_risk_map[0, 0] - 1
            self._explore2()

        return f"The minimum risk found is {int(min_risk)}."
