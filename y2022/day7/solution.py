from adventofcode.y2022.utils import read_data


class FileSystem:
    def __init__(self):
        self.files = {}
        self.dirrs = []

    def add_dir(self, fullpath):
        self.dirrs.append(fullpath.replace("//", "/"))

    def add_file(self, path, name, size):
        path = path.replace("//", "/")
        fullpath = f"{path}/{name}"
        if fullpath in self.files.keys():
            raise Exception(f"File {fullpath} already exists")
        self.files[fullpath] = (path, name, size)

    def __str__(self):
        output = ""
        for k, v in self.files.items():
            output += f"{k} (file={v})\n"
        return output


if __name__ == "__main__":
    puzzle_input = read_data(7, example=False)

    # Part 1
    filesystem = FileSystem()
    filesystem.add_dir("")
    current_path = ""
    line = 0
    while line < len(puzzle_input):
        cmd = puzzle_input[line]
        # print(cmd)
        if cmd.startswith("$ cd"):
            dirr = cmd.split(" ")[-1]
            if dirr == "..":
                current_path = "/".join(current_path.split("/")[:-1])
            else:
                current_path += "/" + dirr
            current_path = current_path.replace("//", "")
            assert current_path in filesystem.dirrs
        elif cmd.startswith("$ ls"):
            line += 1
            while puzzle_input[line][0] != "$" and puzzle_input[line] != "EOF":
                cmd = puzzle_input[line]
                if cmd.startswith("dir"):
                    path = current_path + "/" + cmd.split(" ")[-1]
                    filesystem.add_dir(path)
                else:
                    filesystem.add_file(current_path, cmd.split()[1], int(cmd.split()[0]))
                line += 1
            continue
        line += 1

    print(filesystem)
    directory_sizes = {}
    sum_of_small_dirs = 0
    for directory in filesystem.dirrs:
        # Sum files in directory
        total_size = sum([v[2] for k, v in filesystem.files.items() if v[0] == directory])
        for subdir in filesystem.dirrs:
            if subdir.startswith(directory) and subdir != directory:
                total_size += sum([v[2] for k, v in filesystem.files.items() if v[0] == subdir])
        print(f"Directory {directory} has {total_size} bytes")
        directory_sizes[directory] = total_size
        if total_size < 100000:
            sum_of_small_dirs += total_size

    print(f"Sum of small directories: {sum_of_small_dirs}")

    # Part 2
    TOTAL_AVAILBALE_SPACE = 70000000
    space_left = TOTAL_AVAILBALE_SPACE - directory_sizes[""]
    need_to_free_at_least = 30000000 - space_left

    print(f"Space left: {space_left}. Need to free at least: {need_to_free_at_least}")
    closest = ""
    closest_size = 10000000000000
    for directory, size in directory_sizes.items():
        if need_to_free_at_least < size < closest_size:
            closest = directory
            closest_size = size

    print(f"Closest directory is {closest} with size {closest_size}")
