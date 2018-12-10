def read_input(file_name):
    with open(file_name) as f:
        return f.readlines()

def min_idx(l):
    return min(xrange(len(l)), key=l.__getitem__)
