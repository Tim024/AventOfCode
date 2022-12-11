from adventofcode.utils import AbstractSolution


class Monkey:
    def __init__(self, string_block):
        self.name = string_block[0].replace(':', '')
        self.starting_items = eval('[' + string_block[1].strip('Starting items:') + ']')
        self.operation_str = string_block[2].replace('Operation: new =', '')
        self.div = int(string_block[3].strip('Test: divisible by '))
        self._if_true = int(string_block[4].strip('If true: throw to monkey '))
        self._if_false = int(string_block[5].replace('If false: throw to monkey ', ''))

    def _test(self, item):
        return self._if_true if item % self.div == 0 else self._if_false

    def cycle(self):
        actions = []
        for item in self.starting_items:
            item = eval(self.operation_str.replace('old', str(item)))
            # item = int(item / 3) # Only part 1
            actions.append((item, self._test(item)))
        self.starting_items = []
        return actions

    def __repr__(self):
        return self.name


class Solution(AbstractSolution):

    def parse(self, puzzle_input: list[str]) -> None:
        self.monkeys = []
        monkey_blocks = []
        for i in range(len(puzzle_input)):
            l = puzzle_input[i]
            if l == '':
                self.monkeys.append(Monkey(monkey_blocks))
                monkey_blocks = []
            else:
                monkey_blocks.append(l)
            if i == len(puzzle_input) - 1:
                self.monkeys.append(Monkey(monkey_blocks))

    def part1(self) -> str:

        inspected_items = {m: 0 for m in self.monkeys}
        for round in range(20):
            for m in self.monkeys:
                inspected_items[m] += len(m.starting_items)
                actions = m.cycle()
                for item, id in actions:
                    self.monkeys[id].starting_items.append(item)

        two_most = sorted(inspected_items.values(), reverse=True)[:2]
        return f'After 20 rounds, the monkeys have inspected {inspected_items} items. The mult is {two_most[0] * two_most[1]}.'

    def part2(self) -> str:

        inspected_items = {m: 0 for m in self.monkeys}

        modulo_factor = 1
        for m in self.monkeys:
            modulo_factor *= m.div

        for round in range(10000):
            for m in self.monkeys:
                inspected_items[m] += len(m.starting_items)
                actions = m.cycle()
                for item, id in actions:
                    self.monkeys[id].starting_items.append(item % modulo_factor)

        two_most = sorted(inspected_items.values(), reverse=True)[:2]
        return f'After 10000 rounds, the monkeys have inspected {inspected_items} items. The mult is {two_most[0] * two_most[1]}.'
