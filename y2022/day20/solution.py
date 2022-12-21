from adventofcode.utils import AbstractSolution, parse_puzzle_input
import numpy as np


class Solution(AbstractSolution):
    def parse(self, puzzle_input: str) -> None:
        self.numbers = parse_puzzle_input(puzzle_input, delimiter="\n")

        # self.numbers1 = [f"{n}_index{i}" for i, n in enumerate(self.numbers)]
        # self.numbers2 = self.numbers1.copy()
        # for n in self.numbers1:
        #     current_index = self.numbers2.index(n)
        #     current_number = int(n.split("_")[0])
        #     self.numbers2 = np.delete(self.numbers2, current_index).tolist()
        #     # print(f"Deleted {n} from self.numbers2: {self.numbers2}")
        #     new_pos = (current_index + current_number) % len(self.numbers2)
        #     if new_pos == 0:
        #         self.numbers2.append(n)
        #     else:
        #         self.numbers2 = np.insert(self.numbers2, new_pos, n).tolist()
        #     # print(f"Insert {n} to self.numbers2 at {new_pos}: {self.numbers2}")
        #     # print(f"Current index: {current_index}, current number: {current_number}, new position: {new_pos}")
        #     # print(self.numbers2)
        # # print(self.numbers2)

    def part1(self) -> str:
        for i,n in enumerate(self.numbers2):
            if n.startswith("0_"):
                break
        groove_coordinates = [int(self.numbers2[(i+k) % len(self.numbers2)].split('_')[0]) for k in [1000,2000,3000]]
        return f"The groove coordinates are {groove_coordinates}. The sum is {sum(groove_coordinates)}."

    def part2(self) -> str:
        decryption_key = 811589153

        self.numbers1 = [f"{int(n)*decryption_key}_index{i}" for i, n in enumerate(self.numbers)]
        self.numbers2 = self.numbers1.copy()
        print(self.numbers2)
        for retry in range(10):
            for n in self.numbers1:
                current_index = self.numbers2.index(n)
                current_number = int(n.split("_")[0])
                self.numbers2 = np.delete(self.numbers2, current_index).tolist()
                # print(f"Deleted {n} from self.numbers2: {self.numbers2}")
                new_pos = (current_index + current_number) % len(self.numbers2)
                if new_pos == 0 and current_number<0:
                    self.numbers2.append(n)
                else:
                    self.numbers2 = np.insert(self.numbers2, new_pos, n).tolist()
                # print(f"Insert {n} to self.numbers2 at {new_pos}: {self.numbers2}")
            # self.numbers1 = self.numbers2.copy()
            print(self.numbers2)
        for i,n in enumerate(self.numbers2):
            if n.startswith("0_"):
                break
        groove_coordinates = [int(self.numbers2[(i+k) % len(self.numbers2)].split('_')[0]) for k in [1000,2000,3000]]
        return f"The groove coordinates are {groove_coordinates}. The sum is {sum(groove_coordinates)}."
