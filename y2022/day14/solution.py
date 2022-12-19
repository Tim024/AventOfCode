from typing import List
from enum import Enum

from adventofcode.utils import AbstractSolution


class Pixel(Enum):
    AIR = 0
    SAND = 1
    BLOCKED_SAND = 3
    ROCK = 2


class Rocklines:
    def __init__(self, line):

        self.blocked_pixels = []
        coords = line.split(' -> ')
        for val in coords:
            x, y = val.split(',')
            pixel = (int(x), int(y))
            # print(f"Rockline: {pixel}")
            if len(self.blocked_pixels) > 0:
                # print(f"Last pixel: {self.blocked_pixels[-1]}")
                if pixel[0] == self.blocked_pixels[-1][0]:
                    # print(f"\tWe have {pixel[0]} == {self.blocked_pixels[-1][0]}")
                    y21, y22 = pixel[1], self.blocked_pixels[-1][1]
                    if y21 > y22:
                        y21, y22 = y22, y21
                    for y2 in range(y21, y22):
                        # print(f"\t\tAdding pixel: {pixel[0], y2}")
                        self.blocked_pixels.append((pixel[0], y2))
                elif pixel[1] == self.blocked_pixels[-1][1]:
                    # print(f"\tWe have {pixel[1]} == {self.blocked_pixels[-1][1]}")
                    x21 = self.blocked_pixels[-1][0]
                    x22 = pixel[0]
                    if x21 > x22:
                        x21, x22 = x22, x21
                    for x2 in range(x21, x22):
                        # print(f"\t\tAdding pixel: {x2, pixel[1]}")
                        self.blocked_pixels.append((x2, pixel[1]))
                else:
                    raise Exception('Invalid line')
            self.blocked_pixels.append(pixel)


class EndOfSimulation(Exception):
    pass


class Sandfall:
    def __init__(self, rocklines: List[Rocklines]):
        self.step = 0
        self.x_lim = 1000
        self.y_lim = 0
        for r in rocklines:
            for x, y in r.blocked_pixels:
                if y > self.y_lim:
                    self.y_lim = y
        self.y_lim += 3
        self.pixels = [[Pixel.AIR for _ in range(self.y_lim)] for _ in range(self.x_lim)]
        for r in rocklines:
            self.add_rockline(r)
        self.moving_sand = [(500, 0)]
        self.pixels[500][0] = Pixel.SAND

    def add_rockline(self, rockline: Rocklines):
        for x, y in rockline.blocked_pixels:
            self.pixels[x][y] = Pixel.ROCK

    def move_sand(self, x_from, y_from, x_to, y_to):
        if x_to < 0 or x_to >= self.x_lim or y_to < 0 or y_to >= self.y_lim:
            print(f"Sand at {x_from}, {y_from} fell out of the map")
            raise EndOfSimulation
        if self.pixels[x_to][y_to] == Pixel.AIR:
            self.pixels[x_to][y_to] = Pixel.SAND
            self.pixels[x_from][y_from] = Pixel.AIR
            return True
        return False

    def simulate_1step(self):
        self.step += 1
        for x in range(self.x_lim):
            for y in range(self.y_lim - 1, -1, -1):  # From bottom to top
                if self.pixels[x][y] == Pixel.SAND:
                    if not self.move_sand(x, y, x, y + 1):  # Try to move down
                        # print(f"Sand at {x}, {y} can't move down: {self.pixels[x][y + 1]}")
                        if not self.move_sand(x, y, x - 1, y + 1):  # Try move left
                            # print(f"Sand at {x}, {y} can't move left: {self.pixels[x - 1][y + 1]}")
                            if not self.move_sand(x, y, x + 1, y + 1):  # Try to move right
                                # print(f"Sand at {x}, {y} can't move right: {self.pixels[x + 1][y + 1]}")
                                self.pixels[x][y] = Pixel.BLOCKED_SAND
                                if (x, y) in self.moving_sand:
                                    self.moving_sand.remove((x, y))

                                if len(self.moving_sand) == 0:
                                    raise EndOfSimulation
                                else:
                                    # Add a new movable sand
                                    last_known_movable_sand = self.moving_sand[-1]
                                    # print(f"Adding new movable sand at {last_known_movable_sand}")
                                    self.pixels[last_known_movable_sand[0]][last_known_movable_sand[1]] = Pixel.SAND
                            else:
                                self.moving_sand.append((x, y))
                        else:
                            self.moving_sand.append((x, y))
                    else:
                        self.moving_sand.append((x, y))

    def visualize(self):
        import matplotlib.pyplot as plt
        import numpy as np
        sand_x, sand_y = [], []
        rock_x, rock_y = [], []
        for x in range(self.x_lim):
            for y in range(self.y_lim):
                if self.pixels[x][y] == Pixel.SAND or self.pixels[x][y] == Pixel.BLOCKED_SAND:
                    sand_x.append(x)
                    sand_y.append(-y)
                elif self.pixels[x][y] == Pixel.ROCK:
                    rock_x.append(x)
                    rock_y.append(-y)

        plt.scatter(sand_x, sand_y, c='yellow', s=10, marker='s', label='Sand')
        plt.scatter(rock_x, rock_y, c='black', s=10, marker='s', label='Rock')
        plt.grid()
        plt.axis('off')
        plt.legend()
        plt.savefig(f"sandfall_{self.step:03d}.png")
        plt.close()


class Solution(AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        rocklines = []
        for line in puzzle_input:
            rocklines.append(Rocklines(line))
        self.sandfall = Sandfall(rocklines)

    def part1(self) -> str:
        while True:
            try:
                self.sandfall.simulate_1step()
                if self.sandfall.step % 100 == 0:
                    print(f"Step {self.sandfall.step} done")
                    self.sandfall.visualize()
            except EndOfSimulation:
                break

        return f"We have a total of {sum([1 for x in range(self.sandfall.x_lim) for y in range(self.sandfall.y_lim) if self.sandfall.pixels[x][y] == Pixel.BLOCKED_SAND])} blocked sand pixels"

    def part2(self) -> str:
        y_lim = self.sandfall.y_lim -1
        self.sandfall.add_rockline(Rocklines(f"1,{y_lim} -> 999,{y_lim}"))
        return self.part1()
