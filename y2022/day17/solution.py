from adventofcode.utils import AbstractSolution, parse_puzzle_input

# SHAPES = [
#     "####",
#     ".#.\n###\n.#.",
#     "..#\n..#\n###",
#     "#\n#\n#\n#\n#",
#     "##\n##"
# ]
SHAPES = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],  # X,Y for bottom left to top right
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    [(0, 0), (0, 1), (1, 0), (1, 1)]
]


class Piece:
    def __init__(self, shape, x, y):
        self.shape = shape
        self.x = x
        self.y = y
        self.width = max([x for x, y in shape]) + 1
        self.height = max([y for x, y in shape]) + 1

    def collide(self, other):
        for x, y in self.shape:
            for ox, oy in other.shape:
                if self.x + x == other.x + ox and self.y + y == other.y + oy:
                    return True
        return False

    def add(self, other):
        other_at = [(x + other.x, y + other.y) for x, y in other.shape].copy()
        self.shape = self.shape + other_at


class Solution(AbstractSolution):

    def get_max_height(self):
        max_height = max([y for x, y in self.frozen.shape]) if self.frozen.shape else -1
        return max_height + 1

    def visualize(self, current_shape, shape_position, counter):
        import matplotlib.pyplot as plt
        max_height = 20
        max_width = 7
        shape_with_pos = [(x + shape_position[0], y + shape_position[1]) for x, y in current_shape]
        plt.scatter([x for x, y in self.frozen.shape], [y for x, y in self.frozen.shape], c='b')
        plt.scatter([x for x, y in shape_with_pos], [y for x, y in shape_with_pos], c='r')
        plt.xlim(-1, max_width + 1)
        plt.title(f"Counter: {counter}, Shape: {SHAPES.index(current_shape)}, Position: {shape_position}")
        plt.ylim(-1, max_height + 1)
        plt.xticks(range(max_width + 1))
        plt.yticks(range(max_height + 1))
        plt.grid()
        plt.savefig(f"images_{counter:03d}.png")
        plt.close()

    def parse(self, puzzle_input: str) -> None:
        fallen_rocks = 0
        self.frozen = Piece([(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)], 0, 0)
        input_counter = -1
        current_shape = SHAPES[fallen_rocks % len(SHAPES)]
        shape_position = [2, 3 + self.get_max_height()]
        while fallen_rocks < 1000000000000:
            if fallen_rocks % 200 == 0: print(f"Fallen rocks: {fallen_rocks}")
            input_counter += 1
            input = puzzle_input[input_counter % len(puzzle_input)]
            # self.visualize(current_shape, shape_position, input_counter)
            # print(f"Fallen rocks: {fallen_rocks + 1}, "
            #       f"shape: {SHAPES.index(current_shape)}, "
            #       f"position: {shape_position}, input: {input}")

            if input == '<':
                move = [-1, 0]
            elif input == '>':
                move = [1, 0]
            else:
                raise ValueError(f"Unknown input: {input}")
            new_position = [shape_position[0] + move[0], shape_position[1] + move[1]]
            new_piece = Piece(current_shape, new_position[0], new_position[1])
            if not new_piece.collide(self.frozen) and 0 <= new_position[0] <= (7 - new_piece.width):
                shape_position = new_position

            # self.visualize(current_shape, shape_position, input_counter)
            move = [0, -1]
            new_position = [shape_position[0] + move[0], shape_position[1] + move[1]]
            if Piece(current_shape, new_position[0], new_position[1]).collide(self.frozen):
                self.frozen.add(Piece(current_shape, shape_position[0], shape_position[1]))
                fallen_rocks += 1
                current_shape = SHAPES[fallen_rocks % len(SHAPES)]
                shape_position = [2, 3 + self.get_max_height()]
            else:
                shape_position = new_position

    def part1(self) -> str:
        return f"After 2022 rocks, we have a max height of {self.get_max_height()-1}."

    def part2(self) -> str:
        return f"I give up."
