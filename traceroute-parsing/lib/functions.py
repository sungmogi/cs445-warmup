def generate_lines(filename):
    with open(filename, "r") as f:
        for line in f:
            yield line.strip()
