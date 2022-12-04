def read_data(day, example=False, sep='\n', folder="y2022"):
    if example:
        ext = 'example'
    else:
        ext = 'input'
    with open(f"./{folder}/day{day}/data.{ext}") as f:
        return f.read().split(sep)