from enum import Enum
import inspect
import os
import os.path
from pathlib import Path
import re
from typing import Any
from typing import Union
from typing import Type
from unittest import TestCase


def file_exists(file_name):
    root_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(root_path, "../input/{}".format(file_name))

    return os.path.exists(path) and Path(path).is_file()


def read_input(file_name):
    root_path = os.path.abspath(os.path.dirname(__file__))
    input_path = os.path.join(root_path, "../input/{}".format(file_name))
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
        return f"{self.year}/day{self.day}.txt"

    @property
    def input_data(self):
        if file_exists(self.input_file):
            return read_input(self.input_file)

    @property
    def example_input_file(self):
        return f"{self.year}/day{self.day}-test.txt"

    @property
    def example_input_file_pt2(self):
        return f"{self.year}/day{self.day}-pt2-test.txt"

    @property
    def example_input_data(self):
        if file_exists(self.example_input_file):
            return read_input(self.example_input_file)

    @property
    def example_input_data_pt1(self):
        return self.example_input_data

    @property
    def example_input_data_pt2(self):
        if file_exists(self.example_input_file_pt2):
            return read_input(self.example_input_file_pt2)
        if file_exists(self.example_input_file):
            return self.example_input_data


class AdventDayRunner:
    def setUp(self):
        self.instance = self.__class__.instance_cls()

    def test_part_1_example(self):
        runner = getattr(self.instance, "run_part_1", None)
        if not callable(runner):
            return

        result = runner(self.instance.example_input_data_pt1)

        print(f"{self.__class__.instance_cls.__name__} Part 1 Example Result: {result}")

    def test_part_1(self):
        base_runner = getattr(self.instance, "part_1", None)
        runner = getattr(self.instance, "run_part_1", None)
        result = None
        if callable(base_runner):
            result = base_runner()
        elif callable(runner):
            result = runner(self.instance.input_data)
        else:
            return

        print(f"{self.__class__.instance_cls.__name__} Part 1 Result: {result}")

    def test_part_2_example(self):
        runner = getattr(self.instance, "run_part_2", None)
        if not callable(runner):
            return

        result = runner(self.instance.example_input_data_pt2)

        print(f"{self.__class__.instance_cls.__name__} Part 2 Example Result: {result}")

    def test_part_2(self):
        base_runner = getattr(self.instance, "part_2", None)
        runner = getattr(self.instance, "run_part_2", None)
        result = None
        if callable(base_runner):
            result = base_runner()
        elif callable(runner):
            result = runner(self.instance.input_data)
        else:
            return

        print(f"{self.__class__.instance_cls.__name__} Part 2 Result: {result}")


class AdventPart(Enum):
    PART_1 = 1
    PART_2 = 2


class MissingInputException(Exception):
    pass


class InvalidAdventDay(Exception):
    pass


def calling_module_name():
    frame = inspect.currentframe()
    # look back by 2 frames since the first frame will be this function's caller
    caller_frame = frame.f_back.f_back
    module = inspect.getmodule(caller_frame)
    file_path = inspect.getfile(module)
    return module.__name__


DAY_PATTERN_STR = r"Day(\d+)"
DAY_PATTERN = re.compile(DAY_PATTERN_STR)
YEAR_PATTERN_STR = r"y(\d+)"
YEAR_PATTERN = re.compile(YEAR_PATTERN_STR)


class AdventDayV2:
    def __init__(self, year=None, day=None):
        self.year = None
        if year:
            self.year = year
        else:
            super_module = calling_module_name()
            module_parts = super_module.split(".")

            for part in module_parts:
                m = YEAR_PATTERN.match(part)
                if m and m.group(1):
                    self.year = int(m.group(1))
                    break

            if not self.year:
                raise InvalidAdventDay(
                    f"Invalid Advent Day: {super_module}.{self.__class__.__name__}"
                )

        if day:
            self.day = day
        else:
            m = DAY_PATTERN.match(self.__class__.__name__)
            if m and m.group(1):
                self.day = int(m.group(1))
            else:
                raise InvalidAdventDay(f"Invalid Advent Day: {self.__class__.__name__}")

    def input_file_pt1(self, example=False):
        if example:
            return f"{self.year}/day{self.day}-pt1-test.txt"
        else:
            return f"{self.year}/day{self.day}-pt1.txt"

    def input_file_pt2(self, example=False):
        if example:
            return f"{self.year}/day{self.day}-pt2-test.txt"
        else:
            return f"{self.year}/day{self.day}-pt2.txt"

    def input_file_base(self, example=False):
        if example:
            return f"{self.year}/day{self.day}-test.txt"
        else:
            return f"{self.year}/day{self.day}.txt"

    def input_file(self, part: AdventPart, example: bool = False):
        specific_input = None
        if part == AdventPart.PART_1:
            specific_input = self.input_file_pt1(example)
        elif part == AdventPart.PART_2:
            specific_input = self.input_file_pt2(example)

        if specific_input and file_exists(specific_input):
            return specific_input
        else:
            f = self.input_file_base(example)
            if file_exists(f):
                return self.input_file_base(example)
            else:
                raise MissingInputException(
                    f"No input file found for {self.year} Day {self.day} {part} Example: {example}"
                )

    def read_input_file(self, part: AdventPart, example: bool = False):
        return read_input(self.input_file(part, example))

    def get_parser(self, input, part: AdventPart):
        parser = None
        if part == AdventPart.PART_1:
            p = getattr(self, "parse_part_1", None)
            if callable(p):
                return p
        elif part == AdventPart.PART_2:
            p = getattr(self, "parse_part_2", None)
            if callable(p):
                return p

        if not parser:
            p = getattr(self, "parse_input", None)
            if callable(p):
                return p

        return lambda input: input

    def run(self, part: AdventPart, example: bool = False):
        input = self.read_input_file(part, example)
        parser = self.get_parser(input, part)
        if part == AdventPart.PART_1:
            return self.run_part_1(parser(input))
        elif part == AdventPart.PART_2:
            return self.run_part_2(parser(input))

    def run_part_1(self, input):
        raise NotImplementedError()

    def run_part_2(self, input):
        raise NotImplementedError()

    class Tests(TestCase):
        instance_cls: Any = None
        EXPECTED: dict[Union[tuple[int, bool], tuple[AdventPart, bool]], Any] = {}

        def setUp(self):
            self.instance = self.__class__.instance_cls()

        def validate(self, result, part: AdventPart, example: bool):
            if self.__class__.EXPECTED:
                expected = None
                if (part.value, example) in self.__class__.EXPECTED:
                    expected = self.__class__.EXPECTED[(part.value, example)]
                elif (part, example) in self.__class__.EXPECTED:
                    expected = self.__class__.EXPECTED[(part, example)]

                if expected:
                    self.assertEqual(expected, result)

        def render(self, result, part: AdventPart, example: bool):
            if example:
                example_text = " Example"
            else:
                example_text = ""

            if self.__class__.instance_cls:
                instance = self.__class__.instance_cls
                print(
                    f"Y{self.instance.year} Day{self.instance.day} Pt{part.value}{example_text}: {result}"
                )
                self.validate(result, part, example)

        def test_part_1_example(self):
            try:
                res = self.instance.run(AdventPart.PART_1, example=True)
                self.render(res, AdventPart.PART_1, example=True)
            except MissingInputException:
                pass

        def test_part_1(self):
            res = self.instance.run(AdventPart.PART_1, example=False)
            self.render(res, AdventPart.PART_1, example=False)

        def test_part_2_example(self):
            try:
                res = self.instance.run(AdventPart.PART_2, example=True)
                self.render(res, AdventPart.PART_2, example=True)
            except MissingInputException:
                pass

        def test_part_2(self):
            res = self.instance.run(AdventPart.PART_2, example=False)
            self.render(res, AdventPart.PART_2, example=False)
