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

        self.distances = {v: {} for v in self.graph.keys()}
        for v in self.graph.keys():
            self.compute_distances(v, v)

        self.cache = {t:() for t in range(44)}

        if self.example:
            print(f"Flow rates: {self.flows}")
            print(f"Graph: {self.graph}")
            print(f"Distances: {self.distances}")

    def compute_distances(self, valve, current_valve, visited=None, distance=0):
        if visited is None:
            visited = []
        visited.append(current_valve)
        for v in self.graph[current_valve]:
            if v not in visited:
                if v in self.distances[valve].keys():
                    self.distances[valve][v] = min(distance + 1, self.distances[valve][v])
                else:
                    self.distances[valve][v] = distance + 1
                self.compute_distances(valve, v, visited + [v], distance + 1)

    def _compute_options(self, valve, opened_valves):
        options = {nb: dist for nb, dist in self.distances[valve].items() if nb not in opened_valves}
        return options

    def explore(self, valve, time_left, opened_valves, flow, authorized_valves=None):
        key = (valve, tuple(opened_valves))
        if key in self.cache[time_left]:
            return self.cache[time_left][key]

        options = self._compute_options(valve, opened_valves)
        new_flow = flow
        max_flow = new_flow
        # Open valve VALVE if not opened and not 0
        if valve not in opened_valves and self.flows[valve] != 0 and (authorized_valves is None or valve in authorized_valves):
            time_left -= 1
            new_flow += self.flows[valve] * time_left
            opened_valves.append(valve)
        # For each other unopened valve
        for nb, dist in options.items():
            if nb not in opened_valves and self.flows[nb] != 0 and (authorized_valves is None or nb in authorized_valves):
                time_left_for_option = time_left - dist
                if time_left_for_option > 0:
                    path_flow = self.explore(nb, time_left_for_option, opened_valves.copy(), new_flow, authorized_valves=authorized_valves)
                    max_flow = max(max_flow, path_flow)
        max_flow = max(max_flow, new_flow)
        return max_flow

    def part1(self) -> str:
        time_left = 30
        max_flow = self.explore('AA', time_left, [], 0)
        return f"The maximum flow is {max_flow} when starting from 'AA'."

    def part2(self) -> str:
        max_flow = 0
        time_left = 26
        import itertools
        import numpy as np
        all_valves = list(k for k in self.flows.keys() if self.flows[k] != 0)
        authorized_valves = [list(c) for i in range(len(all_valves) -1) for c in itertools.combinations(all_valves, i + 1)]
        authorized_valves = np.array(authorized_valves)
        np.random.shuffle(authorized_valves)
        for a in authorized_valves:
            human_valves = a
            elephant_valves = [v for v in all_valves if v not in human_valves]
            flow = self.explore('AA', time_left, [], 0, human_valves) + self.explore('AA', time_left, [], 0, elephant_valves)
            max_flow = max(max_flow, flow)
            # print(f"Max flow with {human_valves} and {elephant_valves} is {flow} {max_flow}")
        return f"The maximum flow is {max_flow}."
