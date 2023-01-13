from adventofcode.utils import AbstractSolution, parse_puzzle_input


class Solution(AbstractSolution):
    def parse(self, puzzle_input: str) -> None:
        self.lines = parse_puzzle_input(puzzle_input)
        self.sc = {')': 3, ']': 57, '}': 1197, '>': 25137}
        self.op = ['(', '[', '{', '<']
        self.cl = [')', ']', '}', '>']

    def part1(self) -> str:
        score = 0
        self.incomplete = []
        for l in self.lines:
            opened = []
            for c in l:
                if c in self.op:
                    opened.append(c)
                elif c in self.cl:
                    idx = self.cl.index(c)
                    if len(opened) == 0 or opened[-1] != self.op[idx]:
                        score += self.sc[c]
                        opened = []
                        break
                    else:
                        del opened[-1]
            if len(opened) != 0:
                self.incomplete.append(opened)
        return f"The final score is {score}."

    def part2(self) -> str:
        sc = {')': 1, ']': 2, '}': 3, '>': 4}
        scores = []
        for op in self.incomplete:
            score = 0
            for i in range(len(op)-1, -1, -1):
                closing = self.cl[self.op.index(op[i])]
                score = score*5 + sc[closing]
            scores.append(score)
        scores = sorted(scores)
        return f"The final middle score is {scores[int(len(scores)/2)]}."
