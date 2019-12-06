from unittest import TestCase

from shared import read_input

class Day1:
    @staticmethod
    def fuel(mass):
        return max(0, int(int(mass) / 3) - 2)

    @staticmethod
    def total_fuel(mass):
        total_fuel = 0

        fuel = Day1.fuel(mass)
        while fuel > 0:
            total_fuel += fuel
            fuel = Day1.fuel(fuel)

        return total_fuel


class Day1Tests(TestCase):
    def test_part_1_example(self):
        assert Day1.fuel(12) == 2
        assert Day1.fuel(14) == 2
        assert Day1.fuel(1969) == 654
        assert Day1.fuel(100756) == 33583

    def test_part_1(self):
        data = read_input('y2019-day1-input.txt')

        out = sum([Day1.fuel(mass) for mass in data])
        print(out)

    def test_part_1_example(self):
        assert Day1.total_fuel(14) == 2
        assert Day1.total_fuel(1969) == 966
        assert Day1.total_fuel(100756) == 50346

    def test_part_2(self):
        data = read_input('y2019-day1-input.txt')

        out = sum([Day1.total_fuel(mass) for mass in data])
        print(out)

