from adventofcode.utils import AbstractSolution, parse_puzzle_input


class Solution(AbstractSolution):
    def parse(self, puzzle_input: str) -> None:
        self.insts = [(p.split(' ')[0],int(p.split(' ')[1])) for p in parse_puzzle_input(puzzle_input)]

    def part1(self) -> str:
        fwd, dpth = 0, 0
        for i in self.insts:
            if i[0] == "forward": fwd += i[1]
            elif i[0] == "down": dpth += i[1]
            elif i[0] == "up": dpth -= i[1]
        return f"The result is {fwd*dpth}."

    def part2(self) -> str:
        fwd, dpth,aim = 0, 0, 0
        for i in self.insts:
            if i[0] == "forward":
                fwd += i[1]
                dpth += aim * i[1]
            elif i[0] == "down":
                aim += i[1]
            elif i[0] == "up":
                aim -= i[1]
        return f"The result is {fwd*dpth}."
