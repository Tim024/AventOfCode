from adventofcode.utils import AbstractSolution


class Solution(AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        self.signal_strengths = {20 + i * 40: None for i in range(6)}

        # Insert extra instruction before addx:
        cycle_aligned_input = []
        for l in puzzle_input:
            if l.startswith("addx"):
                cycle_aligned_input.append("pre " + l)
            cycle_aligned_input.append(l)

        cycle = 1
        X = 1
        self.X_moves = {1: 1}
        for l in cycle_aligned_input:
            ls = l.split()
            if ls[0] == 'noop':
                pass
            elif ls[0] == 'pre':
                pass
            elif ls[0] == 'addx':
                X += int(ls[1])
                self.X_moves[cycle] = X
            else:
                raise Exception(f"Unknown instruction {ls[0]}")
            cycle += 1

            if cycle in self.signal_strengths.keys():
                self.signal_strengths[cycle] = X * cycle
            if cycle >= 240:
                break

    def part1(self) -> str:
        return f"The signal strength are {self.signal_strengths}. The sum is {sum(self.signal_strengths.values())}"

    def part2(self) -> str:
        pixels = ""

        X = 1
        for cycle in range(1, 240):
            if cycle % 40 - 2 <= X <= cycle % 40:
                pixels += "X"
            else:
                pixels += " "

            if cycle in self.X_moves.keys():
                X = self.X_moves[cycle]

        pixel_array = ""
        for i in range(6):
            pixel_array += pixels[i * 40:(i + 1) * 40] + "\n"
        return f"The pixel array is:\n{pixel_array}"
