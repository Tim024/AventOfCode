from adventofcode.utils import AbstractSolution, parse_puzzle_input


class Solution(AbstractSolution):
    def parse(self, puzzle_input: str) -> None:
        pos, instr = parse_puzzle_input(puzzle_input, delimiter='\n', block_delimiter='\n\n')
        self.pos = set((int(p.split(',')[0]), int(p.split(',')[1])) for p in pos)
        self.instr = []
        for i in instr:
            xy = 1 if i.split('=')[0][-1] == 'y' else 0
            self.instr.append((xy, int(i.split('=')[1])))

    def _display(self):
        for y in range(0, max(self.pos, key=lambda x: x[1])[1] + 1):
            for x in range(0, max(self.pos, key=lambda x: x[0])[0] + 1):
                print('██' if (x, y) in self.pos else '  ', end='')
            print()

    def part1(self) -> str:
        self.visibles = []
        for xy, s in self.instr:
            new_pos = set()
            if xy == 1:
                for x, y in self.pos:
                    new_pos.add((x, s - abs(y - s)))
            else:
                for x, y in self.pos:
                    new_pos.add((s - abs(x - s), y))
            self.pos = new_pos
            self.visibles.append(len(self.pos))
        return f"After {len(self.instr)} foldings, we have {len(self.pos)} unique positions. After one folding, we have {self.visibles[0]} visible dots."

    def part2(self) -> str:
        self._display()
        return f""
