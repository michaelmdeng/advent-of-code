from unittest import TestCase

from shared import AdventDay, AdventDayRunner


class Day1(AdventDay):
    def __init__(self):
        AdventDay.__init__(self, 2022, 1)

    def part_1(self):
        lines = self.input_data
        elves = []
        elf = []
        for line in lines:
            if len(line.strip()) == 0:
                elves.append(elf)
                elf = []
            else:
                elf.append(int(line.strip()))

        max_elf = max(elves, key=lambda elf: sum(elf))
        return sum(max_elf)

    def part_2(self):
        lines = self.input_data
        elves = []
        elf = []
        for line in lines:
            if len(line.strip()) == 0:
                elves.append(elf)
                elf = []
            else:
                elf.append(int(line.strip()))

        elves_sorted_by_calories = sorted(elves, key=lambda elf: -sum(elf))
        top_3_elves = elves_sorted_by_calories[:3]
        return sum([sum(elf) for elf in top_3_elves])


class Day1Tests(AdventDayRunner, TestCase):
    instance_cls = Day1
