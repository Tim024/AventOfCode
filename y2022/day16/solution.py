from adventofcode.utils import AbstractSolution, parse_puzzle_input


class Solution(AbstractSolution):
    def parse(self, puzzle_input: str) -> None:
        lines = parse_puzzle_input(puzzle_input)
        self.flows = {}
        self.graph = {}
        for l in lines:
            v = l.split('Valve ')[1].split(' ')[0]
            f = int(l.split(' has flow rate=')[1].split(';')[0])
            o = l.split(';')[-1].replace(' tunnels lead to valves ', '').replace(' tunnel leads to valve ', '').replace(' ', '').split(',')
            self.flows[v] = f
            self.graph[v] = o

    # def queue_score(self, queue):
    #     unique_valves = set()
    #     score = 0
    #     minutes = 0
    #     output = ""
    #     for v in queue:
    #         output += f"You move to valve {v}.\n"
    #         minutes += 1
    #         output += f"== Minute {minutes} ==\n"
    #         if v not in unique_valves and self.flows[v] > 0:
    #             unique_valves.add(v)
    #             output += f"You open valve {v}.\n"
    #             minutes += 1
    #             output += f"== Minute {minutes} ==\n"
    #             score += self.flows[v] * (30 - minutes)
    #             # print(f"Opened {v}. Adding flow {self.flows[v]}*(30 - {minutes})={self.flows[v] * (30 - minutes)} to score at minute {minutes}")
    #         output += f"Valves {unique_valves} are opened, releasing {sum([self.flows[v] for v in unique_valves])}.\n"
    #     print(output)
    #     return score

    def explore(self, state):
        pass


    def part1(self) -> str:
        queue = []
        self.seen_stats = []
        # self.explore('AA', queue)
        # self.explore('BB', queue)
        # print(out)
        # print(paths)
        return "I give up"

    def part2(self) -> str:
        return "I give up"
