from adventofcode.utils import AbstractSolution, parse_puzzle_input
import numpy as np


class Solution(AbstractSolution):
    def parse(self, puzzle_input: str) -> None:
        mapp = np.array(list(map(list, parse_puzzle_input(puzzle_input))))
        mapp[mapp == '#'] = 1
        mapp[mapp == '.'] = 0
        self.map = mapp.astype(int)

        self.__directions = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1), 'NE': (-1, 1), 'NW': (-1, -1), 'SE': (1, 1), 'SW': (1, -1)}
        self.__orders = ['N', 'S', 'W', 'E']

    def check_move(self, x, y, dx, dy):
        if 0 <= x + dx < self.map.shape[0] and 0 <= y + dy < self.map.shape[1]:
            if self.map[x + dx, y + dy] == 1:
                # print(f"\t\t Cant move {x+dx}, {y+dy}")
                return 1  # Someone is in the way
            else:
                # print(f"\t\t Can move {x+dx}, {y+dy}")
                return 0  # No one is in the way
        # print(f"\t\t OOB {x+dx}, {y+dy}")
        return 2  # Out of bounds

    def move(self, x, y):
        # Check all direction
        map = {}
        for d, (dx, dy) in self.__directions.items():
            map[d] = self.check_move(x, y, dx, dy)
        # Check if is alone
        if all([m % 2 == 0 for m in map.values()]):
            # print(f"\t Alone")
            return x, y
        # Check move
        for dir in self.__orders:
            check = [check for check in self.__directions.keys() if dir in check]
            # print(f"Checking {dir} {[map[c] % 2 == 0 for c in check]}")
            if all([map[c] % 2 == 0 for c in check]):
                # print(f"\t Can move {dir}")
                return x + self.__directions[dir][0], y + self.__directions[dir][1]
        # print(f"\t Cant move")
        return x, y

    def visualize(self, counter):
        import matplotlib.pyplot as plt
        idx = np.argwhere(self.map == 1)
        xs = idx[:, 0]
        ys = idx[:, 1]
        plt.scatter(ys, xs, marker='s', s=5, c='k')
        plt.xlabel('Y (W -> E)')
        plt.ylabel('X (S -> N)')
        plt.ylim(plt.ylim()[::-1])
        plt.figaspect(1)
        plt.grid()
        plt.savefig(f"map_{counter:03d}.png")
        plt.clf()

    def part1(self) -> str:
        for iteration in range(10):
            # self.visualize(iteration)
            new_positions = []
            old_positions = []
            for x in range(self.map.shape[0]):
                for y in range(self.map.shape[1]):
                    if self.map[x, y] == 1:
                        nx, ny = self.move(x, y)
                        # print(f"Moving {x}, {y} to {nx}, {ny}")
                        old_positions.append([x, y])
                        if [nx, ny] in new_positions:
                            idx = new_positions.index([nx, ny])
                            new_positions.append([x, y])
                            new_positions[idx] = old_positions[idx]
                        else:
                            new_positions.append([nx, ny])

            max_x = max([x for x, y in new_positions])
            max_y = max([y for x, y in new_positions])
            min_x = min([x for x, y in new_positions])
            min_y = min([y for x, y in new_positions])
            self.map = np.zeros((max_x - min_x + 1, max_y - min_y + 1))
            for x, y in new_positions:
                self.map[x - min_x, y - min_y] = 1

            self.__orders = np.roll(self.__orders, -1)
            # print(f"New orders: {self.__orders}")
        elves = int(np.sum(self.map))
        ground_tiles = int(self.map.shape[0] * self.map.shape[1] - elves)
        return f"The map is {self.map.shape[0]}x{self.map.shape[1]} with {elves} elves and {ground_tiles} ground tiles."

    def part2(self) -> str:
        previous_positions = []
        for iteration in range(10, 1000000):
            new_positions = []
            old_positions = []
            for x in range(self.map.shape[0]):
                for y in range(self.map.shape[1]):
                    if self.map[x, y] == 1:
                        nx, ny = self.move(x, y)
                        # print(f"Moving {x}, {y} to {nx}, {ny}")
                        old_positions.append([x, y])
                        if [nx, ny] in new_positions:
                            idx = new_positions.index([nx, ny])
                            # print(f"Collision at {nx}, {ny}, removing both {old_positions[idx]} {idx}")
                            new_positions.append([x, y])
                            new_positions[idx] = old_positions[idx]
                        else:
                            new_positions.append([nx, ny])

            max_x = max([x for x, y in new_positions])
            max_y = max([y for x, y in new_positions])
            min_x = min([x for x, y in new_positions])
            min_y = min([y for x, y in new_positions])
            self.map = np.zeros((max_x - min_x + 1, max_y - min_y + 1))
            for x, y in new_positions:
                self.map[x - min_x, y - min_y] = 1

            self.__orders = np.roll(self.__orders, -1)
            # print(f"New orders: {self.__orders}")

            # if iteration % 50 == 0:
            #     print(f"Iteration {iteration}")
            #     self.visualize(iteration)
            #     elevs_moving = set([p[0]*1000000+p[1] for p in new_positions]) - set([p[0]*1000000+p[1] for p in previous_positions])
            #     print(f"\tSet diff = {elevs_moving}")
            #     print(f"\tLength diff = {len(elevs_moving)}")

            if new_positions == previous_positions:
                break
            previous_positions = new_positions
        elves = int(np.sum(self.map))
        ground_tiles = int(self.map.shape[0] * self.map.shape[1] - elves)
        return f"The map is {self.map.shape[0]}x{self.map.shape[1]} with {elves} elves and {ground_tiles} ground tiles. Stopped after {iteration} iterations."
