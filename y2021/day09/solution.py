from adventofcode.utils import AbstractSolution, parse_puzzle_input
import numpy as np

class Solution(AbstractSolution):
    def parse(self, puzzle_input: str) -> None:
        self.map = parse_puzzle_input(puzzle_input, block_delimiter="\n", delimiter="", as_array=True).astype(int)
        self.mi, self.mj = self.map.shape

    def part1(self) -> str:
        self.low_points = []
        score = 0
        for i,r in enumerate(self.map):
            for j,c in enumerate(r):
                if i > 0 and self.map[i,j] >= self.map[i-1,j]:
                    continue
                if i < self.mi-1 and self.map[i,j] >= self.map[i+1,j]:
                    continue
                if j > 0 and self.map[i,j] >= self.map[i,j-1]:
                    continue
                if j < self.mj-1 and self.map[i,j] >= self.map[i,j+1]:
                    continue
                score += 1+c
                self.low_points.append((i,j))
        return f"The final score is {score}."

    def fill(self, x, y):
        if self.map[x,y] < 9:
            self.filled_points.add((x,y))
            if x > 0 and self.map[x,y] < self.map[x-1,y]:
                self.fill(x-1,y)
            if x < self.mi-1 and self.map[x,y] < self.map[x+1,y]:
                self.fill(x+1,y)
            if y > 0 and self.map[x,y] < self.map[x,y-1]:
                self.fill(x,y-1)
            if y < self.mj-1 and self.map[x,y] < self.map[x,y+1]:
                self.fill(x,y+1)

    def part2(self) -> str:
        sizes = []
        for i,j in self.low_points:
            self.filled_points = set()
            self.fill(i,j)
            sizes.append(len(self.filled_points))
        l = sorted(sizes, reverse=True)[:3]
        return f"The length of the three largest is {l}. The product is {l[0]*l[1]*l[2]}."

