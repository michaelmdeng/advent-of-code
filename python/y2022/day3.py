import itertools
from unittest import TestCase

from shared import AdventDay, AdventDayRunner


class Day3(AdventDay):
    def __init__(self):
        AdventDay.__init__(self, 2022, 3)

    def priority(self, item):
        if item.isupper():
            return ord(item) - ord("A") + 27
        else:
            return ord(item) - ord("a") + 1

    def part_1(self):
        input = self.input_data

        total = 0
        for line in input:
            rucksack = line.strip()
            compartment1 = set(rucksack[: len(rucksack) // 2])
            compartment2 = set(rucksack[len(rucksack) // 2 :])

            common = compartment1.intersection(compartment2)
            for item in common:
                break

            if item:
                total += self.priority(item)

        return total

    def part_2(self):
        input = self.input_data

        groups = []
        group = []
        for line in input:
            rucksack = line.strip()
            group.append(set(rucksack))
            if len(group) >= 3:
                groups.append(group)
                group = []

        total = 0
        for group in groups:
            common = group[0].intersection(group[1]).intersection(group[2])
            for badge in common:
                break

            print(common)

            total += self.priority(badge)

        return total


class Day3Tests(AdventDayRunner, TestCase):
    instance_cls = Day3
