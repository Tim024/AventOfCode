import numpy as np

from adventofcode.utils import AbstractSolution, parse_puzzle_input


class Solution(AbstractSolution):
    def parse(self, puzzle_input: str) -> None:
        self.octo = parse_puzzle_input(puzzle_input, block_delimiter='\n', delimiter='', as_array=True).astype(int)
        self.octo_original = self.octo.copy()

    def _step(self) -> int:
        self.octo += 1
        fl = np.where(self.octo >= 10)
        while len(fl[0]) > 0:
            self.octo = np.where(self.octo >= 10, 0, self.octo)
            for x, y in zip(*fl):
                for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)):
                    if 0 <= x + dx < self.octo.shape[0] and 0 <= y + dy < self.octo.shape[1]:
                        if self.octo[x + dx, y + dy] != 0:
                            self.octo[x + dx, y + dy] += 1
            fl = np.where(self.octo >= 10)
        return len(np.where(self.octo == 0)[0])

    def part1(self) -> str:
        flashes = 0
        for s in range(100):
            flashes += self._step()
        return f"The number of flashes is {flashes} after 100 steps."

    def part2(self) -> str:
        self.octo = self.octo_original.copy()
        c = 1
        while True:
            f = self._step()
            if f == self.octo.shape[0] * self.octo.shape[1]:
                break
            c += 1
        return f"The first time all octopi are synchronized is {c} steps."
