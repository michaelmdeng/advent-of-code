from unittest import TestCase

from shared import AdventDay, AdventDayRunner

class Day6(AdventDay):
    def __init__(self):
        AdventDay.__init__(self, 2022, 6)

    def part_1(self):
        sequence = self.input_data[0].strip()

        for start_idx in range(0, len(sequence) - 4):
            buffer = sequence[start_idx:start_idx + 4]
            if len(set(buffer)) == 4:
                return start_idx + 4

        return -1

    def part_2(self):
        sequence = self.input_data[0].strip()

        for start_idx in range(0, len(sequence) - 14):
            buffer = sequence[start_idx:start_idx + 14]
            if len(set(buffer)) == 14:
                return start_idx + 14

        return -1


class Day6Tests(AdventDayRunner, TestCase):
    instance_cls = Day6
