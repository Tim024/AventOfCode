from adventofcode.utils import AbstractSolution, parse_puzzle_input

import matplotlib.pyplot as plt
import numpy as np


class Map:
    def __init__(self, width, height, obstacles, ground):
        self.w = width
        self.h = height
        self.obstacles = obstacles
        self.ground = ground
        self.facing = 'E'
        self.__marker = {'N': '^', 'E': '>', 'S': 'v', 'W': '<'}
        self.__turn = {'L': {'N': 'W', 'E': 'N', 'S': 'E', 'W': 'S'},
                       'R': {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}}
        self.__move = {'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)}

    def facing_score(self):
        return {'E': 0, 'S': 1, 'W': 2, 'N': 3}[self.facing]

    def move(self, position, amount):
        dx, dy = self.__move[self.facing]
        previous_position = position
        for i in range(amount):
            new_position = ((previous_position[0] + dx) % self.w, (previous_position[1] + dy) % self.h)
            if new_position in self.obstacles:
                return previous_position
            if new_position not in self.ground:
                # Find new ground in this direction
                for j in range(1, 200):
                    new_position = ((previous_position[0] + j * dx) % self.w, (previous_position[1] + j * dy) % self.h)
                    if new_position in self.obstacles:
                        return previous_position
                    if new_position in self.ground:
                        position = new_position
                        break
            previous_position = new_position
        return previous_position

    def rotate(self, direction):
        self.facing = self.__turn[direction][self.facing]

    def draw(self, position=(0, 0), previous_positions=None, counter=0, title=None):
        plt.figure(figsize=(20, 20))
        ox, oy = np.array(self.obstacles).T
        plt.scatter(ox, oy, marker='s', color='black')
        gx, gy = np.array(self.ground).T
        plt.scatter(gx, gy, marker='s', color='green', alpha=0.3)
        if previous_positions:
            px, py = np.array(previous_positions).T
            plt.scatter(px, py, marker='.', color='blue')
        plt.scatter(position[0], position[1], marker=self.__marker[self.facing], color='red')
        plt.xlim(-1, self.w + 1)
        plt.ylim(self.h + 1, -1)
        plt.title(title or f"Counter: {counter}")
        plt.savefig(f'./map_{counter}.png')
        # plt.show()
        plt.clf()

    def move_cubic(self, position, amount):
        dx, dy = self.__move[self.facing]
        previous_position = position
        previous_facing = self.facing
        for i in range(amount):
            new_position = ((previous_position[0] + dx) % self.w, (previous_position[1] + dy) % self.h)
            if new_position in self.obstacles:
                return previous_position
            if new_position not in self.ground:
                # Find new ground in this direction
                # print(f"New wrapping in {self.facing} direction, {previous_position}")
                x, y = previous_position
                if 50 <= x < 100 and self.facing == 'N':  # 1 2
                    # print("1 2 N")
                    self.facing = 'E'
                    new_position = (0, 100 + x)
                elif 100 <= x < 150 and self.facing == 'N':  # 2 8
                    # print("2 8 N")
                    new_position = (x - 100, 199)
                elif 0 <= y < 50 and self.facing == 'W':  # 1 3
                    # print("1 3 W")
                    self.facing = 'E'
                    new_position = (0, 149 - y)
                elif 0 <= y < 50 and self.facing == 'E':  # 8 6
                    # print("8 6 E")
                    self.facing = 'W'
                    new_position = (99, 149 - y)
                elif 50 <= y < 100 and self.facing == 'W':  # 3 5
                    # print("3 5 W")
                    self.facing = 'S'
                    new_position = (y - 50, 100)
                elif 50 <= y < 100 and self.facing == 'E':  # 4 6
                    # print("4 6 E")
                    self.facing = 'N'
                    new_position = (y + 50, 49)
                elif 100 <= x < 150 and self.facing == 'S':  # 4 6
                    # print("4 6 S")
                    self.facing = 'W'
                    new_position = (99, x - 50)
                elif 0 <= x < 50 and self.facing == 'N':  # 3 5
                    # print("3 5 N")
                    self.facing = 'E'
                    new_position = (50, x + 50)
                elif 100 <= y < 150 and self.facing == 'W':  # 3 1
                    # print("3 1 W")
                    self.facing = 'E'
                    new_position = (50, 149 - y)
                elif 100 <= y < 150 and self.facing == 'E':  # 6 8
                    # print("6 8 E")
                    self.facing = 'W'
                    new_position = (149, 149 - y)
                elif 50 <= x < 100 and self.facing == 'S':  # 7 8
                    # print("7 8 S")
                    self.facing = 'W'
                    new_position = (49, 100 + x)
                elif 150 <= y < 200 and self.facing == 'E':  # 7 8
                    # print("7 8 E")
                    self.facing = 'N'
                    new_position = (y - 100, 149)
                elif 0 <= x < 50 and self.facing == 'S':  # 2 8
                    # print("2 8 S")
                    new_position = (x + 100, 0)
                elif 150 <= y < 200 and self.facing == 'W':  # 1 2
                    # print("1 2 W")
                    self.facing = 'S'
                    new_position = (y - 100, 0)
                if new_position in self.obstacles:
                    self.facing = previous_facing
                    return previous_position
                dx, dy = self.__move[self.facing]
                # print(f"\t{self.facing} direction -> {new_position}")
            previous_position = new_position
            previous_facing = self.facing
        return previous_position


class Solution(AbstractSolution):
    def parse(self, puzzle_input: str) -> None:
        self.pzl = parse_puzzle_input(puzzle_input)
        # Parse map
        obstacles, ground = [], []
        width = 0
        height = 0
        for l in self.pzl:
            length = len(l)
            if length > width:
                width = length
            for i, c in enumerate(l):
                if c == "#":
                    obstacles.append((i, height))
                elif c == '.':
                    ground.append((i, height))
            height += 1
            if length == 0:
                break

        self.map = Map(width, height, obstacles, ground)
        instructions = parse_puzzle_input(puzzle_input)[-1]

        self.instructions = []
        i = 0
        while i < len(instructions):
            try:
                d = int(instructions[i:i + 2])
                self.instructions.append(d)
                i += 1
            except ValueError:
                try:
                    d = int(instructions[i:i + 1])
                    self.instructions.append(d)
                except ValueError:
                    self.instructions.append(instructions[i])
            i += 1

    def part1(self) -> str:
        position = (8, 0) if self.example else (50, 0)

        counter = 0
        # self.map.draw(position, counter=counter)
        for instruction in self.instructions:
            if isinstance(instruction, int):
                position = self.map.move(position, instruction)
            else:
                self.map.rotate(instruction)

            counter += 1
            # print(f"Drawing {counter} {position} instruction: {instruction}")
            # self.map.draw(position, counter=counter)
        return f"The final position is {position}. The final password is {(position[1] + 1) * 1000 + (position[0] + 1) * 4 + self.map.facing_score()}."

    def part2(self) -> str:
        position = (8, 0) if self.example else (50, 0)

        counter = 0
        for instruction in self.instructions:
            if isinstance(instruction, int):
                position = self.map.move_cubic(position, instruction)
            else:
                self.map.rotate(instruction)

            counter += 1
        answer = (position[1] + 1) * 1000 + (position[0] + 1) * 4 + self.map.facing_score()
        return f"The final position is {position}. The final password is {answer}."
