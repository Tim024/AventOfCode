from adventofcode.utils import AbstractSolution

_MAP = None
_VISITED_SQUARES = None


def letter_score(letter):
    order = 'SabcdefghijklmnopqrstuvwxyzE'
    return order.index(letter)


def can_move(l1, l2):
    return letter_score(l2) <= letter_score(l1) + 1


class Agent:
    def __init__(self, x, y, path_length):
        global _VISITED_SQUARES
        self.square_value = _MAP[x][y]
        _VISITED_SQUARES[x][y] = path_length
        self.path_length = path_length
        self.x = x
        self.y = y

    def move(self):
        direction = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        new_agents = []
        # Try move left
        for dx, dy in direction:
            x = self.x + dx
            y = self.y + dy
            if x < 0 or y < 0 or x >= len(_MAP) or y >= len(_MAP[0]):
                continue
            if _VISITED_SQUARES[x][y] is not None:
                if _VISITED_SQUARES[x][y] > self.path_length + 1:  # Square has been visited by worse path
                    new_agents.append(Agent(x, y, self.path_length + 1))
                else:
                    continue
                continue
            if not can_move(self.square_value, _MAP[x][y]):
                continue
            new_agents.append(Agent(x, y, self.path_length + 1))
        return new_agents


class Solution(AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        global _MAP, _VISITED_SQUARES
        self._counter = 0
        _MAP = puzzle_input
        _VISITED_SQUARES = [[None for _ in range(len(_MAP[0]))] for _ in range(len(_MAP))]

        self.exploration_agents = []
        for i in range(len(_MAP)):
            for j in range(len(_MAP[0])):
                if _MAP[i][j] == "S":
                    self.exploration_agents.append(Agent(i, j, 0))

    def part1(self) -> str:
        continue_loop = True
        output = ""
        while continue_loop:
            new_agents = []
            for agent in self.exploration_agents:
                if agent.square_value == "E":
                    output += f"Found exit in {agent.path_length} steps."
                    continue_loop = False
                new_agents += agent.move()
            if len(new_agents) == 0:
                continue_loop = False
            self.exploration_agents = new_agents
        return output

    def part2(self) -> str:
        global _VISITED_SQUARES
        _VISITED_SQUARES = [[None for _ in range(len(_MAP[0]))] for _ in range(len(_MAP))]

        for i in range(len(_MAP)):
            for j in range(len(_MAP[0])):
                if _MAP[i][j] == "a":
                    self.exploration_agents.append(Agent(i, j, 0))

        return self.part1()
