from adventofcode.utils import AbstractSolution, parse_puzzle_input


class SNAFU:
    def __init__(self, number: str or None = None):
        self.s = number
        if self.s is not None:
            self.n = []
            for i in range(len(number)):
                if number[i] == '-':
                    self.n.append(-1)
                elif number[i] == '=':
                    self.n.append(-2)
                else:
                    self.n.append(int(number[i]))
            self.b10 = sum(5 ** (len(self.n) - i - 1) * k for i, k in enumerate(self.n))

    def from_b10(self, b10: int):
        self.b10 = b10
        self.n = []
        while b10 > 0:
            self.n.append(b10 % 5)
            # print(b10 % 5,'added to',self.n,'from',b10)
            b10 //= 5

        self.s = [0 for _ in range(len(self.n) + 1)]

        def add(index, value):
            # Value should be less than 5
            old_v = self.s[index]
            v = (self.s[index] + value + 2) % 5 - 2  # -2, -1, 0, 1, 2
            self.s[index] = v
            if v < 0 <= old_v:
                add(index - 1, 1)

        for i, p in enumerate(self.n[::-1]):
            add(i + 1, p)  # Offset by 2 to keep account for trailing
            # print("Added",self.n,i,p,self.s)

        ids = ['0', '1', '2', '=', '-']
        self.s = ''.join(ids[k] for k in self.s)
        while (self.s[0] == '0'):
            self.s = self.s[1:]


def test():
    test = {
        1: '1',
        2: '2',
        3: '1=',
        4: '1-',
        5: '10',
        6: '11',
        7: '12',
        8: '2=',
        9: '2-',
        10: '20',
        15: '1=0',
        20: '1-0',
        2022: '1=11-2',
        12345: '1-0---0',
        314159265: '1121-1110-1=0'
    }

    for k, v in test.items():
        assert SNAFU(v).b10 == k, f"Test error. '{k}' != '{SNAFU(v).b10}'"

    for k, v in test.items():
        sn = SNAFU()
        sn.from_b10(k)
        assert sn.s == v, f"Test error. '{v}' != '{sn.s}'"

    import numpy as np
    randint = np.random.randint(1, 234234212312312313, 200)
    for r in randint:
        sn = SNAFU()
        sn.from_b10(r)
        assert sn.b10 == r, f"Test error. '{r}' != '{sn.b10}'"


class Solution(AbstractSolution):
    def parse(self, puzzle_input: str) -> None:
        self.snafus = [SNAFU(line) for line in parse_puzzle_input(puzzle_input)]

    def part1(self) -> str:
        summ = sum(sn.b10 for sn in self.snafus)
        s0 = SNAFU()
        s0.from_b10(summ)
        summ_s = s0.s
        return f"The sum of snafus is {summ}. The corresponding SNAFU is {summ_s}."

    def part2(self) -> str:
        return ""
