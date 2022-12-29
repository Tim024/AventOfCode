from adventofcode.utils import AbstractSolution, parse_puzzle_input
import numpy as np


class Solution(AbstractSolution):
    def parse(self, puzzle_input: str) -> None:
        self.bits = parse_puzzle_input(puzzle_input, block_delimiter='\n', delimiter='', as_array=True).astype(int)

    def part1(self) -> str:
        blen = len(self.bits[0])
        gamma = [str(np.bincount(self.bits[:, b]).argmax()) for b in range(blen)]
        epsilon = ''.join(['10'[int(g)] for g in gamma])
        gamma_b10 = int(''.join(gamma), base=2)
        epsilon_b10 = int(epsilon, base=2)
        return f"The gamma is {gamma_b10} and the epsilon is {epsilon_b10}. The product is {gamma_b10 * epsilon_b10}."

    def find(self, b, k, oxygen=True):
        c0 = np.count_nonzero(b[:, k] == 0)
        c1 = np.count_nonzero(b[:, k] == 1)
        if c1 >= c0: v = 1 if oxygen else 0
        else: v = 1 if not oxygen else 0
        nb = [e for e in b if e[k] == v]
        if len(nb) == 1:
            return nb[0]
        return self.find(np.array(nb), k + 1, oxygen=oxygen)


    def part2(self) -> str:
        oxygen = self.find(self.bits, 0, oxygen=True)
        co2 = self.find(self.bits, 0, oxygen=False)
        oxygen_b10 = int(''.join([str(e) for e in oxygen]), base=2)
        co2_b10 = int(''.join([str(e) for e in co2]), base=2)
        return f"The oxygen is {oxygen_b10} and the co2 is {co2_b10}. The product is {oxygen_b10 * co2_b10}."
