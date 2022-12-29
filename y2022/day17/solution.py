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
    # [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
    # [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    # [(0, 0), (0, 1), (0, 2), (0, 3)],
    # [(0, 0), (0, 1), (1, 0), (1, 1)]
]
SHAPE_WIDTH = [4, 3, 3, 1, 2]
MOVES = {'>': 1, '<': -1}

FROZEN_COORDS = {(x, 0) for x in range(7)}


class Piece:
    def __init__(self, id, x, y):
        self.shape = SHAPES[id].copy()
        self.width = SHAPE_WIDTH[id]
        self.x = x
        self.y = y
        self.idd = id

    def __str__(self):
        return f"P{self.idd}({self.x}, {self.y})"

    def __repr__(self):
        return str(self)

    def move(self, input):
        self.x = self.x + MOVES[input]
        # print(f"Piece {self} moved. ({input}, {self.width})")
        if 7 - self.width >= self.x >= 0:
            for x, y in self.shape:
                if (x + self.x, y + self.y) in FROZEN_COORDS:  # X Collision
                    self.x = self.x - MOVES[input]
                    # print(f"Revert jet, blocked position. {x + self.x}, {y + self.y} is blocked by {FROZEN_FRONT_Y[x + self.x]}")
                    break
        else:
            self.x = self.x - MOVES[input]
            # print(f"Revert jet, out of bounds.")

    def fall(self):
        self.y = self.y - 1
        for x, y in self.shape:
            # print(f"\t{x + self.x}, {y + self.y}")
            if (x + self.x, y + self.y) in FROZEN_COORDS:  # Y Collision
                # print(f"Piece {self} frozen. ({FROZEN_FRONT_Y}) Collision at {x+self.x}, {y+self.y}=={FROZEN_FRONT_Y[x+self.x]}")
                self.y += 1  # Revert fall
                return True
        # print(f"Piece {self} falling. ({FROZEN_FRONT_Y})")
        return False

    def update_frozen_front(self):
        global FROZEN_COORDS
        for x, y in self.shape:
            FROZEN_COORDS.add((x + self.x, y + self.y))
        return max(y for x, y in FROZEN_COORDS)


class Solution(AbstractSolution):

    # def visualize(self, current_shape, shape_position, counter):
    #     import matplotlib.pyplot as plt
    #     max_height = 20
    #     max_width = 7
    #     shape_with_pos = [(x + shape_position[0], y + shape_position[1]) for x, y in current_shape]
    #     plt.scatter([x for x, y in self.frozen.shape], [y for x, y in self.frozen.shape], c='b')
    #     plt.scatter([x for x, y in shape_with_pos], [y for x, y in shape_with_pos], c='r')
    #     plt.xlim(-1, max_width + 1)
    #     plt.title(f"Counter: {counter}, Shape: {SHAPES.index(current_shape)}, Position: {shape_position}")
    #     plt.ylim(-1, max_height + 1)
    #     plt.xticks(range(max_width + 1))
    #     plt.yticks(range(max_height + 1))
    #     plt.grid()
    #     plt.savefig(f"images_{counter:03d}.png")
    #     plt.close()

    def parse(self, puzzle_input: str) -> None:
        fallen_rocks = 1
        input_counter = -1
        top = 0
        self.results = {}
        cache = {}
        while fallen_rocks <= 1000000000000:
            p = Piece((fallen_rocks - 1) % len(SHAPES), 2, top + 4)

            while True:
                input_counter += 1
                p.move(puzzle_input[input_counter % len(puzzle_input)])

                collision = p.fall()
                if collision:
                    break
            top = p.update_frozen_front()

            if fallen_rocks in [2022, 1000000000000]:
                self.results[fallen_rocks] = top

            frozen_top = [max(y for x, y in FROZEN_COORDS if x == i) for i in range(7)]
            frozen_top = [y - min(frozen_top) for y in frozen_top]
            key = str((input_counter % len(puzzle_input), fallen_rocks % len(SHAPES), frozen_top))
            if key in cache:
                # print(f"\tCache hit! {cache[key]}")
                rocks = cache[key]
                fallen_rocks += rocks
                # print(f"Total: {fallen_rocks}")
                # FROZEN_COORDS = {(x, y) for x, y in frozen_top}
            cache[key] = fallen_rocks

            # print(f"Now frozen coords is {FROZEN_COORDS}")
            # maxY = max([y for (x, y) in FROZEN_COORDS])
            # for y in range(maxY, 0, -1):
            #     row = ''
            #     for x in range(7):
            #         if (x, y) in FROZEN_COORDS:
            #             row += '#'
            #         else:
            #             row += '.'
            #     print(row)
            # input("Press enter to continue...")

            # if fallen_rocks % 1000000 == 0:
            # print(f"{int(100 * fallen_rocks / 1000000000000)}% rocks fallen.")
            fallen_rocks += 1

    def part1(self) -> str:
        print(self.results)
        return f"Results: {self.results[2022]}."

    def part2(self) -> str:
        return f"After 1000000000000 rocks, we have a max height of {self.results[1000000000000]}."
