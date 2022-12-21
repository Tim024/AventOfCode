from adventofcode.utils import AbstractSolution, parse_puzzle_input


class Solution(AbstractSolution):
    parse_part2 = True

    def parse(self, puzzle_input: str) -> None:
        self.values = {}
        pzle = parse_puzzle_input(puzzle_input, delimiter="\n")
        self.pzle = pzle.copy()

        while len(pzle) > 0:
            for i, line in enumerate(pzle):
                instruction = line.replace(":", "=").replace(" ", "").split("=")
                # Process number first
                try:
                    int(instruction[1])
                    obj = instruction[0]
                    self.values[obj] = int(instruction[1])
                    del pzle[i]
                except:
                    pass

            for i, line in enumerate(pzle):
                instruction = line.replace(":", "=").replace(" ", "").split("=")
                for op in ["+", "*", "-", "/"]:
                    if op in instruction[1]:
                        obj = instruction[0]
                        v1, v2 = instruction[1].split(op)
                        try:
                            self.values[obj] = eval(f"{self.values[v1]}{op}{self.values[v2]}")
                            del pzle[i]
                        except:
                            pass

    def part1(self) -> str:
        return f"Root value is {self.values['root']}."

    def part2(self) -> str:

        # Re-parse the puzzle input differently
        for i, l in enumerate(self.pzle):
            if l.startswith("root"):
                del self.pzle[i]
            if l.startswith("humn"):
                del self.pzle[i]

        self.equation = "pppw==sjmn" if self.example else "jdqw==nrrs"
        self.values_part2 = {}

        for i, line in enumerate(self.pzle):
            instruction = line.replace(":", "=").replace(" ", "").split("=")
            obj = instruction[0]
            self.values_part2[obj] = f"{instruction[1]}"

        while len(self.values_part2) > 0:
            keys_to_delete = []
            for obj, eq in self.values_part2.items():
                if obj in self.equation:
                    self.equation = self.equation.replace(obj, f"({eq})")
                    keys_to_delete.append(obj)
            for k in keys_to_delete:
                del self.values_part2[k]

        print(self.equation)
        rhs, lhs = self.equation.split("==")
        lhs = eval(lhs)
        tens = 10000000000000
        v = 0
        humn_fixed = 0
        humn = 0

        last_4_v = []
        while (eval(rhs) != lhs):
            humn = humn_fixed + tens * v
            print(f"Trying humn={humn} We have {eval(rhs)} > {lhs} == {eval(rhs) > lhs}")
            if eval(rhs) > lhs:
                v += 1
                last_4_v.append(1)
            else:
                v -= 1
                last_4_v.append(-1)
            if len(last_4_v) > 4:
                last_4_v.pop(0)
            if len(last_4_v) == 4 and sum(last_4_v) == 0:
                print(f"Moving out of the loop")
                humn_fixed = humn
                tens = tens / 10
                last_4_v = []

        return f"Human value is {humn}."
