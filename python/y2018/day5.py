from unittest import skip, TestCase

from shared import read_input

INPUT_FILE_PATH = "day5-input.txt"


def process_reactions(chain):
    polys = []

    idx = 0
    while idx < (len(chain) - 1):
        poly_1 = chain[idx]
        poly_2 = chain[idx + 1]

        if poly_1.lower() == poly_2.lower() and poly_1 != poly_2:
            idx += 2
        else:
            polys.append(poly_1)
            idx += 1

    if idx == (len(chain) - 1):
        polys.append(chain[idx])

    return "".join([poly for poly in polys])


def process_all(chain):
    has_reactions = True
    idx = 0
    while has_reactions:
        prev_length = len(chain)
        chain = process_reactions(chain)
        new_length = len(chain)

        has_reactions = new_length != prev_length
        idx += 1

    return chain


def remove_poly(chain, poly):
    return chain.replace(poly.lower(), "").replace(poly.upper(), "")


def main():
    chain = read_input(INPUT_FILE_PATH)[0]
    chain = chain[: len(chain) - 1]  # remove '\n'

    new_chain = process_all(chain)
    print("Part 1: " + str(len(new_chain)))

    lens = [
        len(process_all(remove_poly(chain, poly)))
        for poly in "abcdefghijklmnopqrstuvwyxz"
    ]
    print("Part 2: " + str(max(lens)))


class Day5Tests(TestCase):
    def setUp(self):
        pass

    @skip("Long running test.")
    def test(self):
        main()
