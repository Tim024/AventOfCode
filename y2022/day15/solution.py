from adventofcode.utils import AbstractSolution, parse_puzzle_input
import numpy as np


class BlockedRange:
    def __init__(self):
        self.ranges = []

    def add(self, start, end):
        # print(f"Adding {start} to {end} to blocked ranges for this x")
        if len(self.ranges) == 0:
            self.ranges = [[start, end]]
        else:
            self.ranges.append([start, end])
        # Sort ranges
        self.ranges = sorted(self.ranges, key=lambda x: x[0])
        # Merge ranges
        i = 0
        while i < len(self.ranges) - 1:
            if self.ranges[i][1] >= self.ranges[i + 1][0]:
                self.ranges[i][1] = max(self.ranges[i][1], self.ranges[i + 1][1])
                del self.ranges[i + 1]
            else:
                i += 1


class Solution(AbstractSolution):
    def parse(self, puzzle_input: str) -> None:
        lines = parse_puzzle_input(puzzle_input)

        self.blocked_ranges = {}  # 1 blocked range per x
        self.sensor_and_beacon_positions = []
        for l in lines:
            sensor_x = int(l.split(",")[0].split("=")[1])
            sensor_y = int(l.split(",")[1].split("=")[1].split(":")[0])
            beacon_x = int(l.split("x=")[2].split(",")[0])
            beacon_y = int(l.split("y=")[2].split(":")[0])
            self.sensor_and_beacon_positions.append((sensor_x, sensor_y))
            self.sensor_and_beacon_positions.append((beacon_x, beacon_y))
            brange = np.sum(np.abs(np.array([sensor_x, sensor_y]) - np.array([beacon_x, beacon_y])))

            for i in range(0, brange):
                y = sensor_y + i
                # print(f"On y={y} i={i}")
                if y not in self.blocked_ranges:
                    self.blocked_ranges[y] = BlockedRange()
                self.blocked_ranges[y].add(sensor_x - brange + i, sensor_x + brange - i)
                if i != 0:
                    y2 = sensor_y - i
                    # print(f"On x={x2}")
                    if y2 not in self.blocked_ranges:
                        self.blocked_ranges[y2] = BlockedRange()
                    self.blocked_ranges[y2].add(sensor_x - brange + i, sensor_x + brange - i)

    def part1(self) -> str:
        y = 10 if self.example else 2000000
        b = self.blocked_ranges[y]
        sensor_and_beacon_xs = set([xi for xi, yi in self.sensor_and_beacon_positions if yi == y])
        count = 0
        for r in b.ranges:
            count += r[1] - r[0] + 1
            count -= len([xi for xi in sensor_and_beacon_xs if r[0] <= xi <= r[1]])
        return f"The number of points that can be reached is {count}"

    def part2(self) -> str:
        lim = 20 if self.example else 4000000
        for y in range(0, lim):
            br = self.blocked_ranges[y]
            sensor_and_beacon_xs = set([xi for xi, yi in self.sensor_and_beacon_positions if yi == y])
            spots = lim + 1
            for r in br.ranges:
                a, b = max(0, r[0]), min(lim, r[1])
                spots -= b - a + 1
            if spots == 1:
                for x in range(0, lim):
                    if x not in sensor_and_beacon_xs and not any([r[0] <= x <= r[1] for r in br.ranges]):
                        return f"The location of the only point that can be reached is {x}, {y}. Frequency = {x * 4000000 + y}"
        return ""
