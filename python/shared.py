import os


def read_input(file_name):
    root_path = os.path.abspath(os.path.dirname(__file__))
    input_path = os.path.join(root_path, '../input/{}'.format(file_name))
    with open(input_path) as f:
        return f.readlines()


def min_idx(l):
    return min(range(len(l)), key=l.__getitem__)


class AdventDay:
    def __init__(self, year, day):
        self.year = year
        self.day = day

    @property
    def input_file(self):
        return f'{self.year}/day{self.day}.txt'

    @property
    def input_data(self):
        return read_input(self.input_file)
