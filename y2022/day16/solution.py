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

    def explore(self, valve, time_left, opened_valves, flow):
        options = self._compute_options(valve, opened_valves)
        new_flow = flow
        max_flow = new_flow
        # Open valve VALVE if not opened and not 0
        if valve not in opened_valves and self.flows[valve] != 0:
            time_left -= 1
            new_flow += self.flows[valve] * time_left
            opened_valves.append(valve)
        # For each other unopened valve
        for nb, dist in options.items():
            if nb not in opened_valves and self.flows[nb] != 0:
                time_left_for_option = time_left - dist
                if time_left_for_option > 0:
                    path_flow = self.explore(nb, time_left_for_option, opened_valves.copy(), new_flow)
                    max_flow = max(max_flow, path_flow)
        max_flow = max(max_flow, new_flow)
        return max_flow

    def explore_with_elephant(self):
        return 0

    def part1(self) -> str:
        time_left = 30
        max_flow = self.explore('AA', time_left, [], 0)
        return f"The maximum flow is {max_flow} when starting from 'AA'."

    def part2(self) -> str:
        time_left = 26
        max_flow = self.explore_with_elephant()
        return f"The maximum flow is {max_flow}."
