from unittest import TestCase

from shared import AdventDay, AdventDayRunner

class Day5(AdventDay):
    def __init__(self):
        AdventDay.__init__(self, 2022, 5)

    def move(self, stacks, amt, frm, to):
        for _ in range(0, amt):
            crate = stacks[frm - 1].pop()
            stacks[to - 1].append(crate)

    def move_9001(self, stacks, amt, frm, to):
        frm_stack = stacks[frm - 1]
        to_move = frm_stack[len(frm_stack) - amt:]
        stacks[frm - 1] = frm_stack[:len(frm_stack) - amt]
        stacks[to - 1] = stacks[to - 1] + to_move

    def part_1(self):
        input = self.input_data

        layout_lines = []
        procedure_lines = []
        layout_done = False
        for line in input:
            if layout_done:
                procedure_lines.append(line)
            elif len(line.strip()) == 0:
                layout_done = True
            else:
                layout_lines.append(line)

        layout_lines.reverse()
        num_stacks = max([int(idx) for idx in layout_lines[0].split()])
        stacks = [[] for _ in range(0, num_stacks)]
        for line in layout_lines[1:]: 
            for idx in range(0, num_stacks):
                line_idx = 1 + idx * 4
                crate = line[line_idx]

                if crate != ' ':
                    stacks[idx].append(crate)

        for line in procedure_lines:
            _, amt, _, frm, _, to = line.strip().split()
            self.move(stacks, int(amt), int(frm), int(to))

        return ''.join([stack[len(stack) - 1] for stack in stacks])

    def part_2(self):
        input = self.input_data

        layout_lines = []
        procedure_lines = []
        layout_done = False
        for line in input:
            if layout_done:
                procedure_lines.append(line)
            elif len(line.strip()) == 0:
                layout_done = True
            else:
                layout_lines.append(line)

        layout_lines.reverse()
        num_stacks = max([int(idx) for idx in layout_lines[0].split()])
        stacks = [[] for _ in range(0, num_stacks)]
        for line in layout_lines[1:]: 
            for idx in range(0, num_stacks):
                line_idx = 1 + idx * 4
                crate = line[line_idx]

                if crate != ' ':
                    stacks[idx].append(crate)

        for line in procedure_lines:
            _, amt, _, frm, _, to = line.strip().split()
            self.move_9001(stacks, int(amt), int(frm), int(to))

        return ''.join([stack[len(stack) - 1] for stack in stacks])


class Day5Tests(AdventDayRunner, TestCase):
    instance_cls = Day5
