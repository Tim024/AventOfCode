from adventofcode.y2022.utils import read_data


def process_text(text):
    allsums = []
    for c, elf in enumerate(text):
        s = sum([int(x) for x in elf.split("\n") if x])
        print(f"Elf {c + 1} {s}")
        allsums.append(s)
    top3 = sorted(allsums, reverse=True)[:3]
    for c, s in enumerate(top3):
        print(f"Top elf: {s}")
    print(f"Sum of all calories: {sum(top3)}")


if __name__ == "__main__":
    process_text(read_data(1, example=True, sep="\n\n"))
