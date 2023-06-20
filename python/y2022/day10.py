from collections import namedtuple
from unittest import TestCase

from shared import AdventDay, AdventDayRunner


class Day10(AdventDay):
    def __init__(self):
        AdventDay.__init__(self, 2022, 10)

    def run_part_1(self, input) -> int:
        cycle = 1
        register = 1
        strength = []

        for line in input:
            instruction = line.strip().split()

            if instruction[0] == "noop":
                strength.append(cycle * register)
                cycle += 1
            else:  # instruction[0] == 'addx'
                add_value = int(instruction[1])
                strength.append(cycle * register)
                strength.append((cycle + 1) * register)

                register = register + add_value
                cycle += 2

        return sum(strength[19::40])

    def run_part_2(self, input) -> None:
        cycle = 1
        register = 1
        screen: list[list[str]] = []
        row: list[str] = []

        for line in input:
            instruction = line.strip().split()

            if instruction[0] == "noop":
                pix_idx = (cycle - 1) % 40
                if abs(pix_idx - register) <= 1:
                    screen, row = self.draw(screen, row, "#")
                else:
                    screen, row = self.draw(screen, row, ".")

                cycle += 1
            else:  # instruction[0] == 'addx'
                add_value = int(instruction[1])

                pix_idx = (cycle - 1) % 40
                pix_idx_2 = cycle % 40
                if abs(pix_idx - register) <= 1:
                    screen, row = self.draw(screen, row, "#")
                else:
                    screen, row = self.draw(screen, row, ".")

                if abs(pix_idx_2 - register) <= 1:
                    screen, row = self.draw(screen, row, "#")
                else:
                    screen, row = self.draw(screen, row, ".")

                register = register + add_value
                cycle += 2

        if row:
            screen.append(row)
        for row in screen:
            print("".join(row))

    def draw(
        self, screen: list[list[str]], row: list[str], pixel: str
    ) -> tuple[list[list[str]], list[str]]:
        if len(row) >= 40:
            screen.append(row)
            row = [pixel]
        else:
            row.append(pixel)

        return screen, row


class Day10Tests(AdventDayRunner, TestCase):
    instance_cls = Day10
