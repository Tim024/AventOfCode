from adventofcode.y2022.utils import read_data

ITEMS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def priority(item):
    return ITEMS.index(item) + 1


if __name__ == "__main__":
    sacks = read_data(3, example=False)

    # Part 1
    priorities = []
    for sack in sacks:
        s1 = sack[:len(sack) // 2]
        s2 = sack[len(sack) // 2:]
        # Find repeated items
        repeated = set([i for i in s1 if i in s2])
        priorities += [priority(i) for i in repeated]
    print(sum(priorities))

    # Part 2
    priorities = []
    for i in range(0, len(sacks), 3):
        s1 = sacks[i]
        s2 = sacks[i + 1]
        s3 = sacks[i + 2]
        repeated = set([i for i in s1 if i in s2 and i in s3])
        priorities += [priority(i) for i in repeated]
    print(sum(priorities))
