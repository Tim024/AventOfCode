from adventofcode.utils import AbstractSolution, parse_puzzle_input


class Solution(AbstractSolution):
    def parse(self, puzzle_input: str) -> None:
        polymer, reactions = parse_puzzle_input(puzzle_input, delimiter="\n", block_delimiter="\n\n")
        self.poly = polymer[0]
        self.reactions = {}
        for r in reactions:
            a, b = r.split(" -> ")
            self.reactions[a] = (a[0] + b, b + a[1])

        self.pairs = {}
        for i in range(len(self.poly) - 1):
            dbc = self.poly[i:i + 2]
            self._add_to_pairs(dbc, 1)

    def _add_to_pairs(self, dbc, v):
        if dbc not in self.pairs:
            self.pairs[dbc] = 0
        self.pairs[dbc] += v

    def _remove_pair(self, dbc, v):
        self.pairs[dbc] -= v

    def _step(self):
        old = self.pairs.copy()
        for p,v in old.items():
            if v > 0:
                if p in self.reactions:
                    self._add_to_pairs(self.reactions[p][0], v)
                    self._add_to_pairs(self.reactions[p][1], v)
                    self._remove_pair(p, v)

    def _count(self):
        amount = {}
        for p, v in self.pairs.items():
            for c in p:
                if c not in amount:
                    amount[c] = 0
                amount[c] += v
        amount[self.poly[0]] += 1
        amount[self.poly[-1]] += 1
        for c, v in amount.items():
            amount[c] = int(v / 2)
        return list(amount.values())

    def part1(self) -> str:
        for _ in range(10):
            self._step()
        counts = self._count()
        counts.sort()
        return f"The difference of the most common and least common is {counts[-1] - counts[0]}."

    def part2(self) -> str:
        for _ in range(30):
            poly = self._step()
        counts = self._count()
        counts.sort()
        return f"The difference of the most common and least common is {counts[-1] - counts[0]}."
