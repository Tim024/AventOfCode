from adventofcode.utils import AbstractSolution, parse_puzzle_input


class Solution(AbstractSolution):
    def parse(self, puzzle_input: str) -> None:
        self.lines = parse_puzzle_input(puzzle_input)
        self.sc = {')':3, ']': 57, '}': 1197, '>': 25137}
        self.op = ['(', '[', '{', '<']
        self.cl = [')', ']', '}', '>']

    def part1(self) -> str:
        for l in self.lines:
            for i,c in enumerate(l):
                for o in self.op:
                    opened = sum([1 for k in l[:i] if o == k])
                    closed = sum([1 for k in l[:i] if self.cl[self.op.index(o)] == k])
                    if opened >= closed:
                        continue
                    print(f"l[:i]: {l[:i]}, l: {l}, i: {i}, c: {c}, o: {o}, opened: {opened}, closed: {closed}")
            print(l)
            exit(1)


        return f""

    def part2(self) -> str:
        return f""

