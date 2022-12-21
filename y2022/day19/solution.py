from adventofcode.utils import AbstractSolution, parse_puzzle_input


class Blueprint:
    def __init__(self, ore_cost, clay_cost, obsidian_cost, geode_cost):
        self.ore_cost = ore_cost
        self.clay_cost = clay_cost
        self.obsidian_cost = obsidian_cost
        self.geode_cost = geode_cost

        self.ore_amount = 0
        self.clay_amount = 0
        self.obsidian_amount = 0
        self.geode_amount = 0

        self.ore_robot = 1
        self.clay_robot = 0
        self.obsidian_robot = 0
        self.geode_robot = 0

        # Compute target robot numbers for each resource?


    def run_for(self, minutes):
        for minute in range(minutes):
            self.ore_amount += self.ore_robot
            self.clay_amount += self.clay_robot
            self.obsidian_amount += self.obsidian_robot
            self.geode_amount += self.geode_robot

            if self.ore_amount >= self.geode_cost[0] and self.obsidian_amount >= self.geode_cost[1]:
                self.geode_robot += 1
                self.ore_amount -= self.geode_cost[0]
                self.obsidian_amount -= self.geode_cost[1]
            if self.ore_amount >= self.obsidian_cost[0] and self.clay_amount >= self.obsidian_cost[1]:
                self.obsidian_robot += 1
                self.ore_amount -= self.obsidian_cost[0]
                self.clay_amount -= self.obsidian_cost[1]
            if self.ore_amount >= self.clay_cost:
                self.clay_robot += 1
                self.ore_amount -= self.clay_cost
            if self.ore_amount >= self.ore_cost:
                self.ore_robot += 1
                self.ore_amount -= self.ore_cost

            print(f"== Minute {minute+1} ==")
            print(f"Ore: {self.ore_amount} Ore robot: {self.ore_robot}")
            print(f"Clay: {self.clay_amount} Clay robot: {self.clay_robot}")
            print(f"Obsidian: {self.obsidian_amount} Obsidian robot: {self.obsidian_robot}")
            print(f"Geode: {self.geode_amount} Geode robot: {self.geode_robot}")
        return self.geode_amount


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
        maximum_geode = 0
        maxi = -1
        for i,bp in enumerate(self.blueprints):
            print(f"== Blueprint {i+1} ==")
            geode = bp.run_for(24)
            if geode > maximum_geode:
                maximum_geode = geode
                maxi = i
            print(f"Geode: {geode}")
        return f"The maximum number of geodes is {maximum_geode}. From Blueprint {maxi+1}."

    def part2(self) -> str:
        return ""
