from shared import AdventDayV2


class Day1(AdventDayV2):
    def __init__(self):
        super(Day1, self).__init__()

    def parse_input(self, input) -> list[list[int]]:
        elves = []
        elf: list[int] = []
        for line in input:
            if len(line.strip()) == 0:
                elves.append(elf)
                elf = []
            else:
                elf.append(int(line.strip()))

        return elves

    def run_part_1(self, elves):
        max_elf = max(elves, key=lambda elf: sum(elf))
        return sum(max_elf)

    def run_part_2(self, elves):
        elves_sorted_by_calories = sorted(elves, key=lambda elf: -sum(elf))
        top_3_elves = elves_sorted_by_calories[:3]
        return sum([sum(elf) for elf in top_3_elves])


class Day1Tests(AdventDayV2.Tests):
    instance_cls = Day1
    EXPECTED = {
        (1, False): 67622,
        (2, False): 201491,
    }
