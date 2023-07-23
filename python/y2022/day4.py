from shared import AdventDayV2


class Day4(AdventDayV2):
    def __init__(self):
        super(Day4, self).__init__()

    def contains(self, assignment1, assignment2):
        return (
            assignment1[0] >= assignment2[0] and assignment1[1] <= assignment2[1]
        ) or (assignment2[0] >= assignment1[0] and assignment2[1] <= assignment1[1])

    # A --- B
    #    C --- D
    #
    #    A --- B
    # C --- D
    def overlap(self, assignment1, assignment2):
        return (
            assignment2[0] <= assignment1[1] and assignment2[1] >= assignment1[1]
        ) or (assignment1[0] <= assignment2[1] and assignment1[1] >= assignment2[1])

    def run_part_1(self, input):
        count = 0
        for line in input:
            range1, range2 = line.strip().split(",")
            assignment1 = [int(idx) for idx in range1.split("-")]
            assignment2 = [int(idx) for idx in range2.split("-")]

            if self.contains(assignment1, assignment2):
                count += 1

        return count

    def run_part_2(self, input):
        count = 0
        for line in input:
            range1, range2 = line.strip().split(",")
            assignment1 = [int(idx) for idx in range1.split("-")]
            assignment2 = [int(idx) for idx in range2.split("-")]

            if self.overlap(assignment1, assignment2):
                count += 1

        return count


class Day4Tests(AdventDayV2.Tests):
    instance_cls = Day4
    EXPECTED = {
        (1, False): 573,
        (2, False): 867,
    }
