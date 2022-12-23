from adventofcode.utils import AbstractSolution, parse_puzzle_input


class Cube:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

        self.connected = set()

    def connect(self, other):
        co_x = abs(self.x - other.x) == 1 and abs(self.y - other.y) == 0 and abs(self.z - other.z) == 0
        co_y = abs(self.x - other.x) == 0 and abs(self.y - other.y) == 1 and abs(self.z - other.z) == 0
        co_z = abs(self.x - other.x) == 0 and abs(self.y - other.y) == 0 and abs(self.z - other.z) == 1
        if co_x or co_y or co_z:
            self.connected.add(other)
            return True
        return False

    def faces(self):
        return 6 - len(self.connected)


class Solution(AbstractSolution):
    def parse(self, puzzle_input: str) -> None:
        self.cubes = []
        for x, y, z in parse_puzzle_input(puzzle_input, delimiter=',', block_delimiter='\n'):
            new_cube = Cube(int(x), int(y), int(z))
            for other_cube in self.cubes:
                other_cube.connect(new_cube)
                new_cube.connect(other_cube)
            self.cubes.append(new_cube)

    def part1(self) -> str:
        return f"The sum of visible faces is {sum(cube.faces() for cube in self.cubes)}."

    def part2(self) -> str:
        return ""
