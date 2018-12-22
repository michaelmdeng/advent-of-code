import os

def read_input(file_name):
    root_path = os.path.abspath(os.path.dirname(__file__))
    input_path = os.path.join(root_path, '../input/{}'.format(file_name))
    with open(input_path) as f:
        return f.readlines()

def min_idx(l):
    return min(xrange(len(l)), key=l.__getitem__)
