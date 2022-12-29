from adventofcode.utils import AbstractSolution, parse_puzzle_input
import numpy as np

class Solution(AbstractSolution):
    def parse(self, puzzle_input: str) -> None:
        self.m = parse_puzzle_input(puzzle_input, delimiter=",", as_array=True).astype(int)
        self.median = np.median(self.m)

    def part1(self) -> str:
        total_fuel = sum([abs(self.median - m) for m in self.m])
        return f"The total fuel needed is {int(total_fuel)}."

    def part2(self) -> str:
        last_fuel = np.inf
        m = 1
        for k in range(1, 2000):
            fuel = sum([i for c in self.m for i in range(1,abs(m - c) + 1)])
            if fuel > last_fuel:
                break
            m += 1
            last_fuel = fuel
        return f"The total fuel needed is {int(last_fuel)}."

