import os
from unittest import TestCase


def read_input(file_name):
    root_path = os.path.abspath(os.path.dirname(__file__))
    input_path = os.path.join(root_path, '../input/{}'.format(file_name))
    with open(input_path) as f:
        return f.readlines()


def min_idx(l):
    return min(range(len(l)), key=l.__getitem__)


class AdventDay:
    def __init__(self, year, day):
        self.year = year
        self.day = day

    @property
    def input_file(self):
        return f'{self.year}/day{self.day}.txt'

    @property
    def input_data(self):
        return read_input(self.input_file)

    @property
    def example_input_file(self):
        return f'{self.year}/day{self.day}-test.txt'

    @property
    def example_input_data(self):
        return read_input(self.example_input_file)


class AdventDayRunner:
    instance_cls = None

    def setUp(self):
        self.instance = self.__class__.instance_cls()

    def test_part_1_example(self):
        runner = getattr(self.instance, 'run_part_1', None)
        if not callable(runner):
            return

        result = runner(self.instance.example_input_data)

        print(f'{self.__class__.instance_cls.__name__} Part 1 Example Result: {result}')

    def test_part_1(self):
        base_runner = getattr(self.instance, 'part_1', None)
        runner = getattr(self.instance, 'run_part_1', None)
        result = None
        if callable(base_runner):
            result = base_runner()
        elif callable(runner):
            result = runner(self.instance.input_data)
        else:
            return

        print(f'{self.__class__.instance_cls.__name__} Part 1 Result: {result}')

    def test_part_2_example(self):
        runner = getattr(self.instance, 'run_part_2', None)
        if not callable(runner):
            return

        result = runner(self.instance.example_input_data)

        print(f'{self.__class__.instance_cls.__name__} Part 2 Example Result: {result}')


    def test_part_2(self):
        base_runner = getattr(self.instance, 'part_2', None)
        runner = getattr(self.instance, 'run_part_2', None)
        result = None
        if callable(base_runner):
            result = base_runner()
        elif callable(runner):
            result = runner(self.instance.input_data)
        else:
            return

        print(f'{self.__class__.instance_cls.__name__} Part 2 Result: {result}')
