def read_data(day, example=False, sep='\n'):
    if example:
        ext = 'example'
    else:
        ext = 'input'
    with open(f"./input/day{day}.{ext}") as f:
        return f.read().split(sep)