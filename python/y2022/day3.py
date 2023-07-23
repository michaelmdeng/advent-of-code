import itertools

from shared import AdventDayV2


class Day3(AdventDayV2):
    def __init__(self):
        super(Day3, self).__init__()

    def priority(self, item):
        if item.isupper():
            return ord(item) - ord("A") + 27
        else:
            return ord(item) - ord("a") + 1

    def run_part_1(self, input):
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

    def run_part_2(self, input):
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

            total += self.priority(badge)

        return total


class Day3Tests(AdventDayV2.Tests):
    instance_cls = Day3
    EXPECTED = {
        (1, False): 7793,
        (2, False): 2499,
    }
