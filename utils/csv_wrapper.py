import csv
from collections import namedtuple

def save_csv(filename, header, values):
    with open(filename, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(values)

def load_csv(filename, parser_map):
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        Row = namedtuple("Row", header)
        for row in reader:
            data = [parser_map[h](d) for d, h in zip(row, header)]
            yield Row(*data)
