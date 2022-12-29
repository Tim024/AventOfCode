from adventofcode.utils import AbstractSolution, parse_puzzle_input


class Solution(AbstractSolution):
    def parse(self, puzzle_input: str) -> None:
        self.lines = []
        for c1, c2 in parse_puzzle_input(puzzle_input, block_delimiter="\n", delimiter=" -> "):
            # self.print(p)
            self.lines.append((tuple(map(int, c1.split(','))), tuple(map(int, c2.split(',')))))
        self.lines = tuple(self.lines)
        self.overlaps = set()

    def generate_points(self, line):
        x1, y1 = line[0]
        x2, y2 = line[1]
        if x1 == x2:
            return set((x1, y) for y in range(min(y1, y2), max(y1, y2) + 1))
        elif y1 == y2:
            return set((x, y1) for x in range(min(x1, x2), max(x1, x2) + 1))
        else:
            dx = (x2 - x1)/abs(x2 - x1)
            dy = (y2 - y1)/abs(y2 - y1)
            x, y = x1, y1
            points = set()
            while x != x2 or y != y2:
                points.add((x, y))
                x += dx
                y += dy
            points.add((x, y))
            return points

    def count_overlaps(self, lines):
        for i1, l1 in enumerate(lines):
            for l2 in lines[i1 + 1:]:
                p1 = self.generate_points(l1)
                p2 = self.generate_points(l2)
                inter = p1.intersection(p2)
                if len(inter) > 0:
                    self.overlaps = self.overlaps.union(inter)

    def part1(self) -> str:
        lines = [l for l in self.lines if l[0][0] == l[1][0] or l[0][1] == l[1][1]]
        self.count_overlaps(lines)
        return f"The number of overlaps is {len(self.overlaps)}."

    def part2(self) -> str:
        self.overlaps = set()
        self.count_overlaps(self.lines)
        return f"The number of overlaps is {len(self.overlaps)}."
