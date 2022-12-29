import numpy as pd
from datetime import datetime


def get_puzzle_input_(year: int, day: int, example: bool = False) -> str:
    if example:
        ext = "example"
    else:
        ext = "input"
    with open(f"./y{year}/day{day:02d}/data.{ext}", "r") as puzzle_input:
        lines = puzzle_input.read()
    return lines


def parse_puzzle_input(puzzle_input: str, delimiter: str = "\n", block_delimiter: str or None = None, as_array=False) -> list or pd.array:
    if block_delimiter:
        blocks = puzzle_input.split(block_delimiter)
        if as_array:
            return pd.array([parse_puzzle_input(block, delimiter) for block in blocks])
        return [parse_puzzle_input(block, delimiter) for block in blocks]
    else:
        if delimiter != '':
            splitted = puzzle_input.split(delimiter)
        else:
            splitted = list(puzzle_input)
        if as_array:
            return pd.array(splitted)
        return splitted


class AbstractSolution:
    def __init__(
            self,
                 example: bool = False
                 ) -> None:
        self.year = int(self.__class__.__module__.split(".")[1][1:])
        self.day = int(self.__class__.__module__.split(".")[2][3:])

        self.__print = example
        puzzle_input = get_puzzle_input_(self.year, self.day, example)
        if len(puzzle_input) <= 3:
            self.print(f"Input for day {self.day} of year {self.year} looks empty!")

        self.print("Start parsing input...")

        self.parse(puzzle_input)

        self.print("Parsing complete.")

    def print(self, *args, **kwargs):
        if self.__print:
            date_str = datetime.now().strftime("%H:%M:%S.%f")
            print(f"[{date_str}]\t",*args, **kwargs)

    def parse(self, puzzle_input: str) -> None:
        raise NotImplementedError(f"The parser the puzzle input for day {self.day} of year {self.year} isn't implemented yet!")

    def part1(self) -> str:
        raise NotImplementedError(f"Part 1 of the solution for day {self.day} of year {self.year} isn't implemented yet!")

    def part2(self) -> str:
        raise NotImplementedError(f"Part 2 of the solution for day {self.day} of year {self.year} isn't implemented yet!")
