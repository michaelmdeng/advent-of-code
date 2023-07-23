from shared import AdventDayV2


class Day6(AdventDayV2):
    def __init__(self):
        super(Day6, self).__init__()

    def parse_input(self, input) -> list[str]:
        sequence = input[0].strip()
        return sequence

    def run_part_1(self, sequence):
        for start_idx in range(0, len(sequence) - 4):
            buffer = sequence[start_idx : start_idx + 4]
            if len(set(buffer)) == 4:
                return start_idx + 4

        return -1

    def run_part_2(self, sequence):
        for start_idx in range(0, len(sequence) - 14):
            buffer = sequence[start_idx : start_idx + 14]
            if len(set(buffer)) == 14:
                return start_idx + 14

        return -1


class Day6Tests(AdventDayV2.Tests):
    instance_cls = Day6
    EXPECTED = {
        (1, True): 7,
        (1, False): 1198,
        (2, True): 19,
        (2, False): 3120,
    }
