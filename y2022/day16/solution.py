from adventofcode.utils import AbstractSolution, parse_puzzle_input


class Solution(AbstractSolution):
    def parse(self, puzzle_input: str) -> None:
        lines = parse_puzzle_input(puzzle_input)
        for l in lines:
            v = l.split('Valve ')[1].split(' ')[0]
            f = int(l.split(' has flow rate=')[1].split(';')[0])
            o = l.split(';')[-1].replace(' tunnels lead to valves ', '').replace(' tunnel leads to valve ', '').replace(' ', '').split(',')

    def part1(self) -> str:
        return ""

    def part2(self) -> str:
        return "Oops"
