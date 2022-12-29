from adventofcode.utils import AbstractSolution, parse_puzzle_input


class Solution(AbstractSolution):
    def parse(self, puzzle_input: str) -> None:
        pzl = parse_puzzle_input(puzzle_input, delimiter=" | ", block_delimiter="\n")
        self.ins = [i[0].split(' ') for i in pzl]
        self.outs = [i[1].split(' ') for i in pzl]

    def part1(self) -> str:
        total = 0
        for l in [2, 3, 4, 7]:
            for i in range(len(self.ins)):
                total += len(list(filter(lambda x: len(x) == l, self.outs[i])))
        return f"The total number of specific length outputs is {total}."

    def part2(self) -> str:
        total = 0
        for i in range(len(self.ins)):
            map = {1: set(list(filter(lambda x: len(x) == 2, self.ins[i]))[0]),
                   7: set(list(filter(lambda x: len(x) == 3, self.ins[i]))[0]),
                   4: set(list(filter(lambda x: len(x) == 4, self.ins[i]))[0]),
                   8: set(list(filter(lambda x: len(x) == 7, self.ins[i]))[0])}
            # top = map[7] - map[4]
            for e in map[1]:
                m6 = map[8] - {e}
                if m6 in [set(j) for j in self.ins[i]]:
                    map[6] = m6
                    break

            for j in self.ins[i]:
                if len(map[6].symmetric_difference(set(j))) == 1 and set(j) != map[8]:
                    map[5] = set(j)
                    break

            # print()
            br = map[8].symmetric_difference(map[5]).symmetric_difference(map[8].symmetric_difference(map[6]))
            map[9] = map[8].symmetric_difference(br)

            for j in self.ins[i]:
                if len(j) == 6 and set(j) not in [map[6], map[5], map[9]]:
                    map[0] = set(j)
                    break

            br_item = list(br)[0]
            for j in self.ins[i]:
                sj = set(j)
                if sj not in map.values():
                    if br_item in sj:
                        map[2] = sj
                    else:
                        map[3] = sj
            reverse_map = {frozenset(v): k for k, v in map.items()}

            for k,o in enumerate(self.outs[i]):
                total += 10**(3-k)*reverse_map[frozenset(o)]

        return f"The total sum of the outputs is {total}."
