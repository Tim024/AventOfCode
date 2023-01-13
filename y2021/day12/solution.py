from adventofcode.utils import AbstractSolution, parse_puzzle_input


class Solution(AbstractSolution):
    def parse(self, puzzle_input: str) -> None:
        links = parse_puzzle_input(puzzle_input, delimiter="-", block_delimiter="\n")

        self.neighbors = {}
        for a, b in links:
            if a not in self.neighbors:
                self.neighbors[a] = set()
            self.neighbors[a].add(b)
            if b not in self.neighbors:
                self.neighbors[b] = set()
            self.neighbors[b].add(a)
        self.all_paths = []

    def explore(self, current: str, explored: list, part1=False):
        if current in explored and current == 'start':
            return
        if current in explored and current.islower() and part1:
            return
        if current.islower() and not part1:
            if any(explored.count(c) == 2 for c in explored if c.islower()) and current in explored:
                return
        explored.append(current)
        if current == 'end':
            self.all_paths.append(explored)
            return
        for nb in self.neighbors[current]:
            self.explore(nb, explored.copy(), part1=part1)

    def part1(self) -> str:
        self.explore('start',[], part1=True)
        return f"Found {len(self.all_paths)} paths."

    def part2(self) -> str:
        self.all_paths = []
        self.explore('start',[], part1=False)
        # ap = sorted(self.all_paths)
        # for a in ap:
        #     print(a)
        return f"Found {len(self.all_paths)} paths."
