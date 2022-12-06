
from adventofcode.y2022.utils import read_data

if __name__ == "__main__":
    puzzle_input = read_data(6, example=True)

    # Part 1
    for line in puzzle_input:
        for i,c in enumerate(line):
            if i > 3 and len(set(line[i-4:i])) == len(line[i-4:i]):
                print(i)
                break
    
    # Part 2
    for line in puzzle_input:
        for i,c in enumerate(line):
            if i > 13 and len(set(line[i-14:i])) == len(line[i-14:i]):
                print(i)
                break
