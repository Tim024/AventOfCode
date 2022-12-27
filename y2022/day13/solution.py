from functools import cmp_to_key

from adventofcode.utils import AbstractSolution


def compare_values(val1, val2):
    if val1 == val2:
        return "retry"
    elif val1 < val2:
        return "right"
    else:
        return "wrong"


def compare_array(line1, line2):
    for i in range(len(line1)):
        if i > len(line2) - 1:
            return "wrong"
        else:
            output = compare(line1[i], line2[i])
            print(f"Comparing {line1[i]} and {line2[i]}: {output}")
            if output != "retry":
                return output
    if len(line2) > len(line1):
        return "right"
    return "retry"


def compare(line1, line2):
    if isinstance(line1, list) and isinstance(line2, list):
        return compare_array(line1, line2)
    elif isinstance(line1, list) and isinstance(line2, int):
        return compare(line1, [line2])
    elif isinstance(line1, int) and isinstance(line2, list):
        return compare([line1], line2)
    elif isinstance(line1, int) and isinstance(line2, int):
        return compare_values(line1, line2)
    else:
        raise ValueError("Unrecognized types")


class Solution(AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        self.pairs_of_lines = [[]]

        for line in puzzle_input:
            if line == "":
                self.pairs_of_lines.append([])
            else:
                self.pairs_of_lines[-1].append(eval(line))

    def part1(self) -> str:
        right_indices = []
        for idx, (l1, l2) in enumerate(self.pairs_of_lines):
            print(f"Comparing {l1} and {l2}, index {idx}")
            if compare(l1, l2) == "right":
                right_indices.append(idx + 1)
        return f"The sum of the right indices is: {sum(right_indices)}"

    def part2(self) -> str:
        self.all_lines = [[[2]], [[6]]]
        for pair in self.pairs_of_lines:
            self.all_lines.append(pair[0])
            self.all_lines.append(pair[1])

        def sorting_function(l1, l2):
            return 1 if compare(l1, l2) == "right" else -1

        self.all_lines.sort(key=cmp_to_key(sorting_function), reverse=True)
        position_of_2 = self.all_lines.index([[2]]) + 1
        position_of_6 = self.all_lines.index([[6]]) + 1
        return f"The position of 2 is {position_of_2} and the position of 6 is {position_of_6}. The product is {position_of_2 * position_of_6}."
