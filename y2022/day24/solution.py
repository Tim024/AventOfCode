from adventofcode.utils import AbstractSolution, parse_puzzle_input
import matplotlib.pyplot as plt
import numpy as np


class Solution(AbstractSolution):
    def parse(self, puzzle_input: str) -> None:
        self.map = [list(l) for l in parse_puzzle_input(puzzle_input)]
        self.map_width = len(self.map[0])
        self.map_height = len(self.map)
        self.map = np.array(self.map).T
        self.start_position = (1, 0)
        self.end_position = (self.map_width - 2, self.map_height - 1)

        self.blizzards_pos = {'>': [], '<': [], '^': [], 'v': []}
        self.borders = []
        for x in range(self.map_width):
            for y in range(self.map_height):
                for b in self.blizzards_pos.keys():
                    if self.map[x][y] == b:
                        self.blizzards_pos[b].append([x, y])
                if self.map[x][y] == '#':
                    self.borders.append([x, y])

    def move(self, position, target_position):
        # Return all possible moves from this position
        ps = []
        for move in [[0, 1], [0, -1], [1, 0], [-1, 0], [0, 0]]:
            # print(f"Trying move {move}")
            np = (position[0] + move[0], position[1] + move[1])
            if np == target_position:
                # print("Found the end!")
                return [np], True
            if np[0] < 0 or np[0] >= self.map_width or np[1] < 0 or np[1] >= self.map_height:
                # print(f"\t{position} -> {np} ) oob")
                continue
            # if self.map[np] == ".":
            if self.map[np] != "#":
                # print(f"\t{position} -> {np} ) yes")
                ps.append(np)  # Add all possible moves
            # else:
            #     print(f"\t{position} -> {np} ) no {self.map[np]}")
        return ps, False

    def blizzard(self):
        blizzards_dir = {'>': (1, 0), '<': (-1, 0), '^': (0, -1), 'v': (0, 1)}
        for k, v in self.blizzards_pos.items():
            dir = blizzards_dir[k]
            new_blizzards_pos = []
            for pos in v:
                new_pos = [pos[0] + dir[0], pos[1] + dir[1]]
                if new_pos[0] <= 0:
                    new_pos[0] = self.map_width - 2
                if new_pos[0] >= self.map_width - 1:
                    new_pos[0] = 1
                if new_pos[1] <= 0:
                    new_pos[1] = self.map_height - 2
                if new_pos[1] >= self.map_height - 1:
                    new_pos[1] = 1
                # self.map[new_pos[0]][new_pos[1]] = k
                # self.map[pos[0]][pos[1]] = '.'  # Remove old blizzard
                new_blizzards_pos.append(new_pos)
            self.blizzards_pos[k] = new_blizzards_pos
            # for pos in new_blizzards_pos:
            #     self.map[pos[0]][pos[1]] = k
        return self.map

    def visualize(self, pos=None, iteration=0):
        plt.scatter(self.start_position[0], self.start_position[1], marker='s', color='green')
        plt.scatter(self.end_position[0], self.end_position[1], marker='s', color='red')
        xb, yb = np.array(self.borders).T
        plt.scatter(xb, yb, marker='x', color='black')
        for k, v in self.blizzards_pos.items():
            if len(v) > 0:
                x, y = np.array(v).T
                plt.scatter(x, y, marker=k)
        if pos is not None:
            x, y = np.array(pos).T
            plt.scatter(x, y, marker='.', s=500)
        plt.xlim(-1, self.map_width)
        plt.ylim(self.map_height, -1)
        plt.grid()
        plt.savefig(f"map{iteration}.png")
        plt.clf()

    def part1(self) -> str:
        # Implement some kind of genetic algorithm to find the shortest path
        positions = [self.start_position]  # All paths to test
        c = 0
        while self.end_position not in positions:
            c += 1
            # if c > 20: break
            print(f"Iteration {c} done... Length of positions: {len(positions)}")

            # Compute all positions from the current positions
            new_positions = []
            finished = False
            for p in positions:
                n, finished = self.move(p, self.end_position)
                new_positions += n
                if finished:
                    new_positions = n
                    break
            positions = list(set(new_positions))  # Remove duplicates

            # Move blizzard
            self.blizzard()
            new_positions = []
            # Remove positions that are now blocked by blizzards
            for x, y in positions:
                p = [x, y]
                p_in_blizzard = False
                for k, v in self.blizzards_pos.items():
                    if p in v:
                        p_in_blizzard = True
                if not p_in_blizzard:
                    new_positions.append(p)

            positions = new_positions

            # self.visualize(positions, c)
            if finished:
                break
        return f"The search finished and took {c} iterations."

    def part2(self) -> str:
        # Implement some kind of genetic algorithm to find the shortest path
        positions = [self.start_position]  # All paths to test
        c = 0
        while self.end_position not in positions:
            c += 1
            # print(f"Iteration {c} done... Length of positions: {len(positions)}")

            # Compute all positions from the current positions
            new_positions = []
            finished = False
            for p in positions:
                n, finished = self.move(p, self.end_position)
                new_positions += n
                if finished:
                    new_positions = n
                    break
            positions = list(set(new_positions))  # Remove duplicates
            if finished:
                break

            # Move blizzard
            self.blizzard()
            new_positions = []
            # Remove positions that are now blocked by blizzards
            for x, y in positions:
                p = [x, y]
                p_in_blizzard = False
                for k, v in self.blizzards_pos.items():
                    if p in v:
                        p_in_blizzard = True
                if not p_in_blizzard:
                    new_positions.append(p)

            positions = new_positions

        print(f"Found the end in {c} iterations.")
        positions = [self.end_position]
        while self.start_position not in positions:
            c += 1
            # print(f"Iteration (WAY BACK) {c} done... Length of positions: {len(positions)} {positions}")

            # Compute all positions from the current positions
            new_positions = []
            finished = False
            for p in positions:
                n, finished = self.move(p, self.start_position)
                new_positions += n
                if finished:
                    new_positions = n
                    break
            positions = list(set(new_positions))  # Remove duplicates
            if finished:
                break
            # print(f"Length of new positions: {len(positions)} {positions} {self.end_position}")

            # Move blizzard
            self.blizzard()
            new_positions = []
            # Remove positions that are now blocked by blizzards
            for x, y in positions:
                p = [x, y]
                p_in_blizzard = False
                for k, v in self.blizzards_pos.items():
                    if p in v:
                        p_in_blizzard = True
                if not p_in_blizzard:
                    new_positions.append(p)
            # print(f"Length of new positions: {len(new_positions)}")

            positions = new_positions
            if len(positions) == 0:
                exit(42)

        print(f"Found the start after {c} iterations.")
        positions = [self.start_position]
        while self.end_position not in positions:
            c += 1
            # print(f"Iteration {c} done... Length of positions: {len(positions)}")

            # Compute all positions from the current positions
            new_positions = []
            finished = False
            for p in positions:
                n, finished = self.move(p, self.end_position)
                new_positions += n
                if finished:
                    new_positions = n
                    break
            positions = list(set(new_positions))  # Remove duplicates
            if finished:
                break

            # Move blizzard
            self.blizzard()
            new_positions = []
            # Remove positions that are now blocked by blizzards
            for x, y in positions:
                p = [x, y]
                p_in_blizzard = False
                for k, v in self.blizzards_pos.items():
                    if p in v:
                        p_in_blizzard = True
                if not p_in_blizzard:
                    new_positions.append(p)

            positions = new_positions

        print(f"Found the end in {c} iterations.")
        return f"The search finished and took {c-2} iterations."
