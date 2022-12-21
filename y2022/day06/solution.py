from adventofcode.utils import AbstractSolution, parse_puzzle_input


class Solution(AbstractSolution):
    def parse(self, puzzle_input: str) -> None:
        self.puzzle_input = parse_puzzle_input(puzzle_input, delimiter="\n")

    def part1(self) -> str:
        for line in self.puzzle_input:
            for i, c in enumerate(line):
                if i > 3 and len(set(line[i - 4:i])) == len(line[i - 4:i]):
                    return f"Found {i}."
        return f"Oopsie."

    def part2(self) -> str:
        for line in self.puzzle_input:
            for i, c in enumerate(line):
                if i > 13 and len(set(line[i - 14:i])) == len(line[i - 14:i]):
                    return f"Found {i}."
        return f"Oopsie."
