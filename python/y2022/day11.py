from collections import deque
from collections.abc import Callable
from functools import reduce
from itertools import filterfalse

from shared import AdventDayV2

MonkeyId = int
WorryLevel = int


class Monkey:
    def __init__(
        self,
        mid: MonkeyId,
        items: deque[WorryLevel],
        op: Callable[[WorryLevel], int],
        divisor: int,
        divisible_monkey: MonkeyId,
        undivisible_monkey: MonkeyId,
    ):
        self.mid = mid
        self.items = items
        self.op = op
        self.divisor = divisor
        self.divisible_monkey = divisible_monkey
        self.undivisible_monkey = undivisible_monkey

        self.inspect_count = 0

    def __str__(self) -> str:
        return f"Monkey {self.mid}: items: {self.items}"

    def test(self, item: WorryLevel) -> MonkeyId:
        if item % self.divisor == 0:
            return self.divisible_monkey
        else:
            return self.undivisible_monkey

    def inspect(self) -> tuple[WorryLevel, MonkeyId]:
        self.inspect_count += 1

        item = self.items.popleft()
        new_worry = self.op(item)
        bored_worry = new_worry // 3
        return bored_worry, self.test(bored_worry)

    def inspect_all(self) -> list[tuple[WorryLevel, MonkeyId]]:
        out = []
        while self.items:
            out.append(self.inspect())

        return out

    def inspect_pt2(self) -> tuple[WorryLevel, MonkeyId]:
        self.inspect_count += 1

        item = self.items.popleft()
        new_worry = self.op(item)
        return new_worry, self.test(new_worry)

    def inspect_all_pt2(self) -> list[tuple[WorryLevel, MonkeyId]]:
        out = []
        while self.items:
            out.append(self.inspect_pt2())

        return out


class Day11(AdventDayV2):
    def __init__(self):
        super(Day11, self).__init__()

    def parse_input(self, input: list[str]) -> list[Monkey]:
        groups: list[list[str]] = []
        group: list[str] = []
        for line in input:
            if not line.strip():
                groups.append(group)
                group = []
            else:
                group.append(line.strip())

        if group:
            groups.append(group)

        monkeys = [self.parse_monkey(group) for group in groups]

        return sorted(monkeys, key=lambda m: m.mid)

    def parse_operation(self, s: str) -> Callable[[WorryLevel], int]:
        rhs = s.split("=")[1]
        tokens = rhs.split()

        def op(item_id: WorryLevel) -> int:
            if tokens[0] == "old":
                operand1 = item_id
            else:
                operand1 = int(tokens[0])

            if tokens[2] == "old":
                operand2 = item_id
            else:
                operand2 = int(tokens[2])

            operation = tokens[1]
            if operation == "+":
                return operand1 + operand2
            elif operation == "*":
                return operand1 * operand2
            elif operation == "-":
                return operand1 - operand2
            else:  # operation == '/':
                return operand1 // operand2

        return op

    def parse_test(self, lines: list[str]) -> tuple[int, MonkeyId, MonkeyId]:
        divisor = int(lines[0].split()[-1])
        monkey_if_true = int(lines[1].split()[-1])
        monkey_if_false = int(lines[2].split()[-1])

        return divisor, monkey_if_true, monkey_if_false

    def parse_monkey(self, lines: list[str]) -> Monkey:
        mid = int(lines[0].split()[1].split(":")[0])
        items = deque(int(s) for s in lines[1].split(":")[1].split(",") if s)
        op = self.parse_operation(lines[2])
        divisor, divisible_monkey, undivisible_monkey = self.parse_test(lines[3:])

        return Monkey(mid, items, op, divisor, divisible_monkey, undivisible_monkey)

    def run_part_1(self, input) -> int:
        monkeys = input
        monkey_dict = {}
        for monkey in monkeys:
            monkey_dict[monkey.mid] = monkey

        for round in range(20):
            for monkey in monkeys:
                throws = monkey.inspect_all()

                for item, next_monkey in throws:
                    monkey_dict[next_monkey].items.append(item)

        inspections = sorted(
            (monkey.inspect_count for monkey in monkeys), key=lambda c: -c
        )
        return inspections[0] * inspections[1]

    def run_part_2(self, input) -> int:
        monkeys = input
        monkey_dict = {}
        for monkey in monkeys:
            monkey_dict[monkey.mid] = monkey

        divisor = reduce(lambda acc, elem: acc * elem.divisor, monkeys, 1)

        for round in range(10000):
            for monkey in monkeys:
                throws = monkey.inspect_all_pt2()

                for item, next_monkey in throws:
                    # we don't need the full item value, just enough to persist the
                    # remainder when divided by any of the monkeys
                    # this can be done by multiplying all the monkeys divisors together
                    item = item % divisor
                    monkey_dict[next_monkey].items.append(item)

        inspections = sorted(
            (monkey.inspect_count for monkey in monkeys), key=lambda c: -c
        )
        return inspections[0] * inspections[1]


class Day11Tests(AdventDayV2.Tests):
    instance_cls = Day11
    EXPECTED = {
        (1, True): 10605,
        (1, False): 110264,
        (2, True): 2713310158,
        (2, False): 23612457316,
    }
