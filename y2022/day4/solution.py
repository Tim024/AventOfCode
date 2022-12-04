from adventofcode.y2022.utils import read_data

if __name__ == "__main__":

    overlaps = 0
    for pairs in read_data(4, example=True):
        pair1, pair2 = pairs.split(",")
        p1 = ''.join([f"[{i}]" for i in list(range(int(pair1.split('-')[0]), 1+int(pair1.split('-')[1])))])
        p2 = ''.join([f"[{i}]" for i in list(range(int(pair2.split('-')[0]), 1+int(pair2.split('-')[1])))])
        if p1 in p2 or p2 in p1:
            overlaps += 1
    print(overlaps)

    # Part 2
    overlaps = 0
    for pairs in read_data(4, example=True):
        pair1, pair2 = pairs.split(",")
        p1 = list(range(int(pair1.split('-')[0]), 1+int(pair1.split('-')[1])))
        p2 = list(range(int(pair2.split('-')[0]), 1+int(pair2.split('-')[1])))

        if any([i in p2 for i in p1]) or any([i in p1 for i in p2]):
            print(f"Overlap: {pairs} {p1} and {p2}")
            overlaps += 1
    print(overlaps)