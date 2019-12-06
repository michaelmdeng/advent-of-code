from unittest import TestCase

import shared

def parse_steps(line):
    uppers = [c for c in line if c.isupper()]
    return (uppers[1], uppers[2])


def build_adjacency(steps):
    adj = {}
    rev_adj = {}
    nodes = {}
    for step in steps:
        nodes[step[0]] = step[0]
        nodes[step[1]] = step[1]
        if step[0] not in adj:
            adj[step[0]] = {}
        adj[step[0]][step[1]] = step[1]

        if step[1] not in rev_adj:
            rev_adj[step[1]] = {}
        rev_adj[step[1]][step[0]] = step[0]

    return (adj, rev_adj, nodes)

def adjacency(steps):
    adj = {}
    rev_adj = {}
    nodes = {}
    for step in steps:
        nodes[step[0]] = step[0]
        nodes[step[1]] = step[1]
        if step[0] not in adj:
            adj[step[0]] = {}
        adj[step[0]][step[1]] = step[1]

        if step[1] not in rev_adj:
            rev_adj[step[1]] = {}
        rev_adj[step[1]][step[0]] = step[0]


    steps = []
    while True:
        (adj, rev_adj, nodes, steps) = process_adj(adj, rev_adj, nodes, steps)
        if len(adj.keys()) <= 0 and len(rev_adj.keys()) <= 0:
            break
    for node in nodes.keys():
        if node not in steps:
            steps += [node]
    return steps

def get_next_steps(adj, rev_adj, nodes, prev_steps=[], comp_steps=[], num_workers=5):
    roots = []
    for node in nodes:
        if node not in rev_adj.keys() and node not in prev_steps and node not in comp_steps:
            roots += [node]

    return sorted(roots)[0:min(num_workers, len(roots))]

def finish_steps(adj, rev_adj, nodes, steps):
    for step in steps:
        if step in adj:
            adj.pop(step)
        to_remove = []
        for key in rev_adj:
            if step in rev_adj[key]:
                rev_adj[key].pop(step)
                if len(rev_adj[key].keys()) == 0:
                    to_remove += [key]
        for remove in to_remove:
            rev_adj.pop(remove)

    return(adj, rev_adj, nodes)


def process_adj(adj, rev_adj, nodes, steps, int_steps = [], num_workers=1):
    roots = []
    for node in nodes:
        if node not in rev_adj.keys() and node not in steps and node not in int_steps:
            roots += [node]

    roots = sorted(roots)[0:min(num_workers, len(roots))]
    for root in roots:
        if root in adj:
            adj.pop(root)
        to_remove = []
        for key in rev_adj:
            if root in rev_adj[key]:
                rev_adj[key].pop(root)
                if len(rev_adj[key].keys()) == 0:
                    to_remove += [key]
        for remove in to_remove:
            rev_adj.pop(remove)

    return (adj, rev_adj, nodes, steps + [root[0]])


def get_time(step):
    return ord(step) - ord('A') + 61

def process_time(adj, rev_adj, nodes, num_workers):
    """ A """
    time = 0
    workers = [0 for idx in range(0, num_workers)]
    worker_steps = [None for idx in range(0, num_workers)]

    comp_steps = {}
    prog_steps = {}
    while True:
        curr_workers = len([True for worker in workers if worker == 0])
        steps = get_next_steps(adj, rev_adj, nodes, prog_steps, comp_steps, num_workers)
        worker_idxs = [idx for idx,v in enumerate(workers) if v == 0]
        for (idx, step) in zip(worker_idxs, steps):
            workers[idx] = get_time(step)
            worker_steps[idx] = step
            prog_steps[step] = step




        # print(steps)
        print(worker_steps)
        # print(workers)
        # print(comp_steps)
        # print(prog_steps)

        time += 1
        for idx in range(len(workers)):
            workers[idx] = max(workers[idx] - 1, 0)
            if workers[idx] == 0 and worker_steps[idx]:
                if worker_steps[idx] in prog_steps:
                    prog_steps.pop(worker_steps[idx])
                comp_steps[worker_steps[idx]] = worker_steps[idx]
                (adj, rev_adj, nodes) = finish_steps(adj, rev_adj, nodes, [worker_steps[idx]])
                worker_steps[idx] = None

        if len(adj.keys()) <= 0 and len(rev_adj.keys()) <= 0 and len([True for step in worker_steps if step]) <= 0:
            break
    print(time)

def main_1():
    lines = shared.read_input('day7-input.txt')

    steps = adjacency([parse_steps(line) for line in lines])
    print(''.join(steps))

def main_2():
    lines = shared.read_input('day7-input.txt')

    (adj, rev_adj, nodes) = build_adjacency([parse_steps(line) for line in lines])
    process_time(adj, rev_adj, nodes, num_workers=5)


class Day7Tests(TestCase):
    def setUp(self):
        pass

    def test_part_1(self):
        main_1()

    def test_part_2(self):
        main_2()
