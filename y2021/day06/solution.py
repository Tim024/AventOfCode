import numpy as np

from adventofcode.utils import AbstractSolution, parse_puzzle_input


class Solution(AbstractSolution):
    def parse(self, puzzle_input: str) -> None:
        p = parse_puzzle_input(puzzle_input, delimiter=',', as_array=True).astype(int)
        self.fish = {k: np.count_nonzero(p == k) for k in range(9)}
        self.print(self.fish)

    def part1(self) -> str:
        for day in range(1, 81):
            f0 = self.fish[0]
            nf = {k: self.fish[k + 1] for k in range(0, 8)}
            nf[6] += f0
            nf[8] = f0
            self.fish = nf

            if day in [18, 80]:
                self.print(f" After {day} days there are {sum(self.fish.values())} fish.")
        return f"There are {sum(self.fish.values())} fish after 80 days."

    def part2(self) -> str:
        for day in range(81, 257):
            f0 = self.fish[0]
            nf = {k: self.fish[k + 1] for k in range(0, 8)}
            nf[6] += f0
            nf[8] = f0
            self.fish = nf
        return f"There are {sum(self.fish.values())} fish after 256 days."
