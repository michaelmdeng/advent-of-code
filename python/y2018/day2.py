from unittest import TestCase

from shared import read_input


INPUT_FILE_PATH = 'day2-input.txt'


def has_n_occurences(word, n):
    ch_app = {}
    for ch in word:
        if ch in ch_app:
            ch_app[ch] += 1
        else:
            ch_app[ch] = 1

    for ch in ch_app:
        if ch_app[ch] == n:
            return True

    return False


def string_dist(word1, word2):
    assert len(word1) == len(
        word2), "Can only compare distance of strings of same length."

    return len(word1) - len(common_string(word1, word2))


def common_string(word1, word2):
    assert len(word1) == len(
        word2), "Can only get common part of strings of same length"

    common = ''
    for idx in range(len(word1)):
        if word1[idx] == word2[idx]:
            common += word1[idx]

    return common


def main_1():
    keys = read_input(INPUT_FILE_PATH)

    num_2 = sum([1 if has_n_occurences(key, 2) else 0 for key in keys])
    num_3 = sum([1 if has_n_occurences(key, 3) else 0 for key in keys])

    print("Result: " + str(num_2 * num_3))


def main_2():
    ids = read_input(INPUT_FILE_PATH)
    for idx in range(len(ids)):
        for rest_idx in range(idx + 1, len(ids)):
            curr_id = ids[idx]
            rest_id = ids[rest_idx]

            if string_dist(curr_id, rest_id) == 1:
                print(common_string(curr_id, rest_id))


class Day2Tests(TestCase):
    def setUp(self):
        pass

    def test_part_1(self):
        main_1()

    def test_part_2(self):
        main_2()
