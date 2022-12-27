from adventofcode.utils import AbstractSolution, parse_puzzle_input


class State:
    def __init__(self):
        self.ore_amount = 0
        self.clay_amount = 0
        self.obsidian_amount = 0
        self.geode_amount = 0
        self.ore_robot = 1
        self.clay_robot = 0
        self.obsidian_robot = 0
        self.geode_robot = 0

    @property
    def score(self):
        return self.clay_robot + self.obsidian_robot + self.geode_robot + self.geode_amount

    def __eq__(self, other):
        return self.ore_amount == other.ore_amount \
            and self.clay_amount == other.clay_amount \
            and self.obsidian_amount == other.obsidian_amount \
            and self.geode_amount == other.geode_amount \
            and self.ore_robot == other.ore_robot \
            and self.clay_robot == other.clay_robot \
            and self.obsidian_robot == other.obsidian_robot \
            and self.geode_robot == other.geode_robot

    def __hash__(self):
        return hash((self.ore_amount, self.clay_amount, self.obsidian_amount, self.geode_amount, self.ore_robot, self.clay_robot, self.obsidian_robot, self.geode_robot))

    def __repr__(self):
        return f"State(ore_amount={self.ore_amount}, clay_amount={self.clay_amount}, obsidian_amount={self.obsidian_amount}, geode_amount={self.geode_amount}, ore_robot={self.ore_robot}, clay_robot={self.clay_robot}, obsidian_robot={self.obsidian_robot}, geode_robot={self.geode_robot})"

    def new_states(self, ore_cost, clay_cost, obsidian_cost, geode_cost):
        new_states = set()
        max_ore_required = max([ore_cost, obsidian_cost[0], geode_cost[0], clay_cost])
        max_clay_required = obsidian_cost[1]
        max_obsidian_required = geode_cost[1]

        # State do nothing if materials are not enough
        if self.ore_amount < max_ore_required or (self.clay_amount < obsidian_cost[1] and self.clay_robot > 0):
            # Do nothing only if wait for ore or clay
            new_state = State()
            new_state.ore_amount = self.ore_amount + self.ore_robot
            new_state.clay_amount = self.clay_amount + self.clay_robot
            new_state.obsidian_amount = self.obsidian_amount + self.obsidian_robot
            new_state.geode_amount = self.geode_amount + self.geode_robot
            new_state.ore_robot = self.ore_robot
            new_state.clay_robot = self.clay_robot
            new_state.obsidian_robot = self.obsidian_robot
            new_state.geode_robot = self.geode_robot
            new_states.add(new_state)
        if self.ore_amount >= ore_cost and self.ore_robot < max_ore_required:
            # print("Create ORE ROBOT")
            new_state = State()
            new_state.ore_amount = self.ore_amount - ore_cost + self.ore_robot
            new_state.clay_amount = self.clay_amount + self.clay_robot
            new_state.obsidian_amount = self.obsidian_amount + self.obsidian_robot
            new_state.geode_amount = self.geode_amount + self.geode_robot
            new_state.ore_robot = self.ore_robot + 1
            new_state.clay_robot = self.clay_robot
            new_state.obsidian_robot = self.obsidian_robot
            new_state.geode_robot = self.geode_robot
            new_states.add(new_state)
        if self.ore_amount >= clay_cost and self.clay_robot < max_clay_required:
            # print("Create CLAY ROBOT")
            new_state = State()
            new_state.ore_amount = self.ore_amount - clay_cost + self.ore_robot
            new_state.clay_amount = self.clay_amount + self.clay_robot
            new_state.obsidian_amount = self.obsidian_amount + self.obsidian_robot
            new_state.geode_amount = self.geode_amount + self.geode_robot
            new_state.ore_robot = self.ore_robot
            new_state.clay_robot = self.clay_robot + 1
            new_state.obsidian_robot = self.obsidian_robot
            new_state.geode_robot = self.geode_robot
            new_states.add(new_state)
        if self.ore_amount >= obsidian_cost[0] and self.clay_amount >= obsidian_cost[1] and self.obsidian_robot < max_obsidian_required:
            # print("Create OBSIDIAN ROBOT")
            new_state = State()
            new_state.ore_amount = self.ore_amount - obsidian_cost[0] + self.ore_robot
            new_state.clay_amount = self.clay_amount - obsidian_cost[1] + self.clay_robot
            new_state.obsidian_amount = self.obsidian_amount + self.obsidian_robot
            new_state.geode_amount = self.geode_amount + self.geode_robot
            new_state.ore_robot = self.ore_robot
            new_state.clay_robot = self.clay_robot
            new_state.obsidian_robot = self.obsidian_robot + 1
            new_state.geode_robot = self.geode_robot
            new_states.add(new_state)
            # new_states = {new_state} # Always better than above
        if self.ore_amount >= geode_cost[0] and self.obsidian_amount >= geode_cost[1]:
            # print("Create GEODE ROBOT")
            new_state = State()
            new_state.ore_amount = self.ore_amount - geode_cost[0] + self.ore_robot
            new_state.clay_amount = self.clay_amount + self.clay_robot
            new_state.obsidian_amount = self.obsidian_amount - geode_cost[1] + self.obsidian_robot
            new_state.geode_amount = self.geode_amount + self.geode_robot
            new_state.ore_robot = self.ore_robot
            new_state.clay_robot = self.clay_robot
            new_state.obsidian_robot = self.obsidian_robot
            new_state.geode_robot = self.geode_robot + 1
            # new_states.add(new_state)
            new_states = {new_state}  # Always better than above
        return new_states


class Blueprint:
    def __init__(self, ore_cost, clay_cost, obsidian_cost, geode_cost):
        self.ore_cost = ore_cost
        self.clay_cost = clay_cost
        self.obsidian_cost = obsidian_cost
        self.geode_cost = geode_cost

        self.visited_states = {k: set() for k in range(33)}

    def visit_state(self, state, minute):
        if state in self.visited_states[minute]:
            # print(f"State {state} already visited at minute {minute}")
            return False
        self.visited_states[minute].add(state)
        return True

    def next_minute(self, state, minute):
        new_states = set(s for s in state.new_states(self.ore_cost, self.clay_cost, self.obsidian_cost, self.geode_cost) if self.visit_state(s, minute))
        return new_states


def DFS(state, blueprint, minutes, max_minutes, max_geodes):
    if minutes == max_minutes:
        return state.geode_amount
    else:
        new_states = blueprint.next_minute(state, minutes)
        max_geodes = max(max_geodes, state.geode_amount)
        for new_state in new_states:
            max_geodes = max(max_geodes, DFS(new_state, blueprint, minutes + 1, max_minutes, max_geodes))
        return max_geodes


class Solution(AbstractSolution):
    def parse(self, puzzle_input: str) -> None:
        blueprints = parse_puzzle_input(puzzle_input)
        self.blueprints = []
        for blueprint in blueprints:
            bp = blueprint.split(":")[1]
            bp = bp.split('.')
            ore_cost = int(bp[0].replace("Each ore robot costs", "").replace("ore", "").strip())
            clay_cost = int(bp[1].replace("Each clay robot costs", "").replace("ore", "").strip())
            obsidian_cost = (int(bp[2].replace("Each obsidian robot costs", "").replace("ore", "").split("and")[0].strip()), int(bp[2].split("and")[1].replace("clay", "").strip()))
            geode_cost = (int(bp[3].replace("Each geode robot costs", "").replace("ore", "").split("and")[0].strip()), int(bp[3].split("and")[1].replace("obsidian", "").strip()))
            self.blueprints.append(Blueprint(ore_cost, clay_cost, obsidian_cost, geode_cost))

    def part1(self) -> str:
        all_geo = []
        for i, bp in enumerate(self.blueprints):
            print(f"== Blueprint {i + 1} ==")
            geode = DFS(State(), bp, 0, 24, 0)
            print(f"Maximum geode: {geode}")
            all_geo.append(geode)

            del bp.visited_states
        return f"The maximum number of geodes is {max(all_geo)}. From Blueprint {all_geo.index(max(all_geo)) + 1}. Result: {sum([(i + 1) * g for i, g in enumerate(all_geo)])}"

    def part2(self) -> str:
        all_geo = []
        mult = 1
        for i, bp in enumerate(self.blueprints):
            if i > 2: break
            print(f"== Blueprint {i + 1} ==")
            geode = DFS(State(), bp, 0, 32, 0)
            print(f"Maximum geode: {geode}")
            mult *= geode

            del bp.visited_states
        return f"The maximum number of geodes is {max(all_geo)}. From Blueprint {all_geo.index(max(all_geo)) + 1}. Result: {mult}"
