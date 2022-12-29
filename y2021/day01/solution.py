from adventofcode.utils import AbstractSolution, parse_puzzle_input


class Solution(AbstractSolution):
    def parse(self, puzzle_input: str) -> None:
        self.n = list(map(int, parse_puzzle_input(puzzle_input)))

    def part1(self) -> str:
        increased = sum(1 for i in range(1, len(self.n)) if self.n[i] > self.n[i - 1])
        return f"The number of increased numbers is {increased}."

    def part2(self) -> str:
        w = [sum(self.n[i:i + 3]) for i in range(len(self.n) - 2)]
        increased = sum(1 for i in range(1, len(w)) if w[i] > w[i - 1])
        return f"The number of increased numbers is {increased}."
