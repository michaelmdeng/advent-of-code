from enum import Enum
from unittest import TestCase

from shared import AdventDay, AdventDayRunner


class Day2(AdventDay):
    class Operation(Enum):
        ADD = 1
        MULT = 2
        HALT = 99

    @staticmethod
    def process_operation(program, idx):
        opcode = program[idx]
        op = Day2.Operation(opcode)

        if op == Day2.Operation.ADD:
            term1_idx = program[idx + 1]
            term1 = program[term1_idx]

            term2_idx = program[idx + 2]
            term2 = program[term2_idx]

            result_idx = program[idx + 3]
            program[result_idx] = term1 + term2

            return (program, idx + 4)

        if op == Day2.Operation.MULT:
            term1_idx = program[idx + 1]
            term1 = program[term1_idx]

            term2_idx = program[idx + 2]
            term2 = program[term2_idx]

            result_idx = program[idx + 3]
            program[result_idx] = term1 * term2

            return (program, idx + 4)

        return (program, -1)

    @staticmethod
    def process_program(program):
        program_idx = 0

        while program_idx >= 0:
            (program, program_idx) = Day2.process_operation(program, program_idx)

        return program

    def __init__(self):
        AdventDay.__init__(self, 2019, 2)

    def program(self):
        """
        Loads the program from the input.

        Treated as a strictly-evaluated function so that the original program
        is loaded correctly each time for Part 2.
        """

        program_str = self.input_data[0]
        prog = [int(code) for code in program_str.split(',')]

        return prog

    def part_1(self):
        prog = self.program()

        prog[1] = 12
        prog[2] = 2

        out_prog = Day2.process_program(prog)
        return out_prog[0]

    def part_2(self):
        for noun in range(0, 100):
            for verb in range(0, 100):
                prog = self.program()

                prog[1] = noun
                prog[2] = verb

                try:
                    out_prog = Day2.process_program(prog)
                except ValueError:
                    continue

                if out_prog[0] == 19690720:
                    return 100 * noun + verb

        raise Exception('Could not find combination.')


class Day2Tests(AdventDayRunner, TestCase):
    instance_cls = Day2

    def test_part_1_example(self):
        assert Day2.process_program([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]) == \
            [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]

        assert Day2.process_program([1, 0, 0, 0, 99]) == [2, 0, 0, 0, 99]
        assert Day2.process_program([2, 3, 0, 3, 99]) == [2, 3, 0, 6, 99]
        assert Day2.process_program([2, 4, 4, 5, 99, 0]) == [
            2, 4, 4, 5, 99, 9801]
        assert Day2.process_program([1, 1, 1, 4, 99, 5, 6, 0, 99]) == \
            [30, 1, 1, 4, 2, 5, 6, 0, 99]
