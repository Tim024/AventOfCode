from adventofcode.utils import AbstractSolution, parse_puzzle_input

STACKS = {}


def move_one(fromm, to):
    global STACKS
    STACKS[to].append(STACKS[fromm].pop())


def move_many(amount, fromm, to):
    global STACKS
    crates_fromm = STACKS[fromm]
    crates_to = STACKS[to]
    moved_crates = crates_fromm[-amount:]
    STACKS[fromm] = crates_fromm[:-amount]
    STACKS[to] = crates_to + moved_crates


def move(amount, fromm, to, part2=False):
    if not part2:
        # Part 1
        for i in range(amount):
            move_one(fromm, to)
    else:
        # Part 2
        move_many(amount, fromm, to)


class Solution(AbstractSolution):
    def parse(self, puzzle_input: str) -> None:
        global STACKS
        puzzle_input = parse_puzzle_input(puzzle_input, delimiter="\n")

        # Parse crates
        line_counter = 0
        line = puzzle_input[line_counter]
        while line != "":
            crates = [line[k:k + 3] for k in range(0, len(line) + 1, 4)]
            if " 1 " not in crates:
                for i, c in enumerate(crates):
                    if c != "   ":
                        if i + 1 not in STACKS:
                            STACKS[i + 1] = []
                        STACKS[i + 1].append(c)

            line_counter += 1
            line = puzzle_input[line_counter]

        # Invert stacks
        for k, v in STACKS.items():
            STACKS[k] = v[::-1]

        # Parse instructions
        line_counter += 1
        while line_counter < len(puzzle_input):
            line = puzzle_input[line_counter]

            instructions = [int(c) for c in line.replace("move ", "").replace("from ", "").replace("to ", "").split(" ")]
            # instructions are: amount/from/to
            amount, fromm, to = instructions
            move(amount, fromm, to, part2=True)
            line_counter += 1

    def part1(self) -> str:
        output = ""
        for k in sorted(STACKS.keys()):
            output += f"Top crate: {k}={STACKS[k][-1]}\n"
        return output

    def part2(self) -> str:
        output = ""
        for k in sorted(STACKS.keys()):
            output += f"Top crate: {k}={STACKS[k][-1]}\n"
        return output


if __name__ == "__main__":
    puzzle_input = read_data(5, example=False)

    # Part 1

    # Part 2
