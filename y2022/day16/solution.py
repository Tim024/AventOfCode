from adventofcode.utils import AbstractSolution, parse_puzzle_input


class Status:
    def __init__(self, flows, open_valves=None, total=0):
        if open_valves is None:
            open_valves = set()
        self.open_valves = open_valves
        self.total = total
        self.flows = flows

    def current_flow(self):
        return sum(self.flows[k] for k in self.open_valves)

    def new_status(self, new_valve, open_valve=True):
        s = Status(self.flows, self.open_valves.copy(), self.total)
        if open_valve:
            # print(f"Opening valve {new_valve}")
            s.open_valves.add(new_valve)
        s.total += self.current_flow()
        return s

    def __eq__(self, other):
        return self.open_valves == other.open_valves

    def __hash__(self):
        v = list(self.open_valves)
        v.sort()
        return hash(str(v))

    def __str__(self):
        v = list(self.open_valves)
        v.sort()
        return f"S[{v},{self.total},{self.current_flow()}]"

    def __repr__(self):
        return self.__str__()


def next_minute(statuses, graph, all_valves):
    new_statuses = [None for _ in all_valves]
    for i, old_status_list in enumerate(statuses):
        if not old_status_list:
            continue
        v = all_valves[i]
        # print(f"On {v} {i}")
        for v_dest in graph[v]:
            # print(f"Going to {v_dest}")
            status_list = set()
            for stat in old_status_list:
                # Open valve if not open
                #     ns = stat.new_status(v_dest, open_valve=True)
                #     status_list.add(ns)
                # if v_dest not in stat.open_valves:
                ns = stat.new_status(v_dest, open_valve=False)
                if len(ns.open_valves) > 0:
                    status_list.add(ns)

            # Add all options to new status
            idx = all_valves.index(v_dest)
            # print(f"Adding {status_list} to {idx} Old new_statuses[idx]: {new_statuses[idx]}")
            if new_statuses[idx] is None:
                new_statuses[idx] = status_list
            else:
                new_statuses[idx] = new_statuses[idx].union(status_list)
            # print(f"Result: {new_statuses[idx]}")
        # Open valve if stay on same node
        if new_statuses[i] is None:
            new_statuses[i] = set([s.new_status(v, open_valve=True) for s in old_status_list])
        else:
            new_statuses[i] = new_statuses[i].union(set([s.new_status(v, open_valve=True) for s in old_status_list]))
    return new_statuses


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

    def part1(self) -> str:
        # return "Done."
        # Old method
        # time_left = 30
        # max_flow = self.explore('AA', time_left, [], 0)
        all_valves = list(self.graph.keys())
        all_valves.sort()
        statuses = [None for v2 in all_valves]
        for v in self.graph['AA']:
            statuses[0] = set([Status(self.flows)])
        for t in range(30):
            statuses = next_minute(statuses, self.graph, all_valves)
            print(statuses)
            # input()
        statuses = next_minute(statuses, self.graph, all_valves)
        max_flow = max(max(k.total for k in s) for s in statuses if s)

        return f"The maximum flow is {max_flow} when starting from 'AA'."

    def part2(self) -> str:
        max_flow = 0

        return f"The maximum flow is {max_flow}."
