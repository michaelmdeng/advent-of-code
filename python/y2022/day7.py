from unittest import TestCase

from shared import AdventDay, AdventDayRunner

class Day7(AdventDay):
    def __init__(self):
        AdventDay.__init__(self, 2022, 7)

    def dir_size(self, dir_map, dir_sizes, dirs, files):
        dir_sum = 0
        for d in dirs:
            if d in dir_sizes:
                dir_sum += dir_sizes[d]
            else:
                dir_size = self.dir_size(dir_map, dir_sizes, dir_map[d][0], dir_map[d][1])
                dir_sum += dir_size
                dir_sizes[d] = dir_size

        return dir_sum + sum(files)

    def part_1(self):
        input = self.input_data

        cmd_outputs = []
        cmd_output = []
        for line in input:
            if line.strip().startswith('$'):
                if cmd_output:
                    cmd_outputs.append(cmd_output)
                cmd_output = [line.strip()]
            else:
                cmd_output.append(line.strip())

        if cmd_output:
            cmd_outputs.append(cmd_output)

        curr_dir = '/'
        dir_map = {}
        for cmd_output in cmd_outputs:
            cmd_line = cmd_output[0]
            parts = cmd_line.split()
            if parts[1] == 'cd':
                target = parts[2]

                if target == '/':
                    curr_dir = '/'
                elif target == '..':
                    parts = curr_dir.split('/')
                    parent_parts = parts[:len(parts) - 2]
                    if len(parent_parts) <= 1:
                        curr_dir = '/'
                    else:
                        curr_dir = '/'.join(parts[:len(parts) - 2]) + '/'
                else:
                    curr_dir += target + '/'
            else:
                output = cmd_output[1:]
                output_dirs = []
                output_files = []
                for output_line in output:
                    parts = output_line.split()
                    if parts[0] == 'dir':
                        output_dirs.append(curr_dir + parts[1] + '/')
                    else:
                        output_files.append(int(parts[0]))
                dir_map[curr_dir] = (output_dirs, output_files)

        dir_sizes = {}
        for d, t in dir_map.items():
            dirs = t[0]
            files = t[1]
            if len(dirs) == 0:
                dir_sizes[d] = sum(files)
            else:
                dir_sizes[d] = self.dir_size(dir_map, dir_sizes, dirs, files)

        return sum({ k:v for k, v in dir_sizes.items() if v <= 100000 }.values())

    def part_2(self):
        input = self.input_data

        cmd_outputs = []
        cmd_output = []
        for line in input:
            if line.strip().startswith('$'):
                if cmd_output:
                    cmd_outputs.append(cmd_output)
                cmd_output = [line.strip()]
            else:
                cmd_output.append(line.strip())

        if cmd_output:
            cmd_outputs.append(cmd_output)

        curr_dir = '/'
        dir_map = {}
        for cmd_output in cmd_outputs:
            cmd_line = cmd_output[0]
            parts = cmd_line.split()
            if parts[1] == 'cd':
                target = parts[2]

                if target == '/':
                    curr_dir = '/'
                elif target == '..':
                    parts = curr_dir.split('/')
                    parent_parts = parts[:len(parts) - 2]
                    if len(parent_parts) <= 1:
                        curr_dir = '/'
                    else:
                        curr_dir = '/'.join(parts[:len(parts) - 2]) + '/'
                else:
                    curr_dir += target + '/'
            else:
                output = cmd_output[1:]
                output_dirs = []
                output_files = []
                for output_line in output:
                    parts = output_line.split()
                    if parts[0] == 'dir':
                        output_dirs.append(curr_dir + parts[1] + '/')
                    else:
                        output_files.append(int(parts[0]))
                dir_map[curr_dir] = (output_dirs, output_files)

        dir_sizes = {}
        for d, t in dir_map.items():
            dirs = t[0]
            files = t[1]
            if len(dirs) == 0:
                dir_sizes[d] = sum(files)
            else:
                dir_sizes[d] = self.dir_size(dir_map, dir_sizes, dirs, files)

        used_space = dir_sizes['/']
        total_space = 70000000
        unused_space = total_space - used_space
        needed_space = 30000000
        need_to_delete = needed_space - unused_space
        possible_dirs = { k:v for k, v in dir_sizes.items() if v >= need_to_delete }
        smallest_dir_delete = sorted(possible_dirs.keys(), key=lambda k: possible_dirs[k])[0]
        return possible_dirs[smallest_dir_delete]


class Day6Tests(AdventDayRunner, TestCase):
    instance_cls = Day7
