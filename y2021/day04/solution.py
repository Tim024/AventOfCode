from adventofcode.utils import AbstractSolution, parse_puzzle_input
import re
import numpy as np

class Solution(AbstractSolution):
    def parse(self, puzzle_input: str) -> None:
        pzl = parse_puzzle_input(puzzle_input, delimiter="\n", block_delimiter="\n\n")
        self.t = np.array(pzl[0][0].split(',')).astype(int)
        self.ms = np.array([[re.findall(r'\d+', r) for r in m] for m in pzl[1:]]).astype(int)

        self.ws, self.tss = self.find_winners()

    def find_winners(self):
        ws, tss = [], []
        for k in range(len(self.t)):
            ts=self.t[:k]
            for i,m in enumerate(self.ms):
                if i+1 not in ws:
                    for j in range(5):
                        if all([n in ts for n in m[:,j]]) or all([n in ts for n in m[j,:]]):
                            ws.append(i + 1)
                            tss.append(ts)
                            break
        return ws, tss

    def part1(self) -> str:
        w,ts = self.ws[0],self.tss[0]
        unmarked = sum(k for k in self.ms[w-1].flatten() if k not in ts)
        return f"The winner is {w} with {unmarked} unmarked numbers. The result is {ts[-1]*unmarked}. Number drawn: {ts}"

    def part2(self) -> str:
        w,ts = self.ws[-1],self.tss[-1]
        unmarked = sum(k for k in self.ms[w-1].flatten() if k not in ts)
        return f"The last winner is {w} with {unmarked} unmarked numbers. The result is {ts[-1]*unmarked}. Number drawn: {ts}"

