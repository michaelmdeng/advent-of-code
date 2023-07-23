from shared import AdventDayV2


class Day2(AdventDayV2):
    def __init__(self):
        super(Day2, self).__init__()

    # A B C - X Y Z - Rock Paper Scissors
    def score(self, abc, xyz):
        if abc == "A":
            if xyz == "X":
                return 1 + 3
            elif xyz == "Y":
                return 2 + 6
            else:
                return 3 + 0
        elif abc == "B":
            if xyz == "X":
                return 1 + 0
            elif xyz == "Y":
                return 2 + 3
            else:
                return 3 + 6
        else:
            if xyz == "X":
                return 1 + 6
            elif xyz == "Y":
                return 2 + 0
            else:
                return 3 + 3

    # A B C - Rock Paper Scissors
    # X Y Z - Lose Draw Win
    def score_2(self, abc, xyz):
        if abc == "A":
            if xyz == "X":
                return 3 + 0
            elif xyz == "Y":
                return 1 + 3
            else:
                return 2 + 6
        elif abc == "B":
            if xyz == "X":
                return 1 + 0
            elif xyz == "Y":
                return 2 + 3
            else:
                return 3 + 6
        else:
            if xyz == "X":
                return 2 + 0
            elif xyz == "Y":
                return 3 + 3
            else:
                return 1 + 6

    def run_part_1(self, input):
        score = 0
        for line in input:
            abc, xyz = line.strip().split()
            score += self.score(abc, xyz)

        return score

    def run_part_2(self, input):
        score = 0
        for line in input:
            abc, xyz = line.strip().split()
            score += self.score_2(abc, xyz)

        return score


class Day2Tests(AdventDayV2.Tests):
    instance_cls = Day2
    EXPECTED = {
        (1, False): 14375,
        (2, False): 10274,
    }
