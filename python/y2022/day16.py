from collections import deque, namedtuple
import itertools
import re
from unittest import TestCase

from shared import AdventDay, AdventDayRunner


ValveScan = namedtuple("ValveScan", ["name", "rate", "connections"])


class Day16(AdventDay):
    def __init__(self):
        AdventDay.__init__(self, 2022, 16)

    def parse_part_1(self, input) -> list[ValveScan]:
        p = re.compile(
            r"Valve ([\w]{2}) has flow rate=(\d+); tunnels? leads? to valves? (.*)"
        )

        out = []
        for line in input:
            match_opt = p.match(line.strip())
            if match_opt:
                match = match_opt
                valve = match.group(1)
                flow = match.group(2)
                cxns = match.group(3)
                connections = cxns.split(", ")

                out.append(ValveScan(valve, int(flow), connections))

        return out

    def traverse(self, scan_map: dict[str, ValveScan]) -> dict[tuple[str, str], int]:
        searched = {}
        traverse_map = {}
        for valve in scan_map:
            if valve in searched or scan_map[valve].rate == 0:
                continue

            curr_searched = {}
            search_queue: deque[tuple[str, int]] = deque()
            search_queue.append((valve, 0))
            while search_queue:
                curr, steps = search_queue.popleft()
                curr_searched[curr] = True

                map_key = (min(valve, curr), max(valve, curr))
                traverse_map[map_key] = steps
                for next_valve in scan_map[curr].connections:
                    if next_valve not in curr_searched:
                        search_queue.append((next_valve, steps + 1))

            searched[valve] = True

        return traverse_map

    def max_released(
        self,
        t: int,
        max_t: int,
        curr: str,
        opened: dict[str, bool],
        scan_map: dict[str, ValveScan],
        traversal_map: dict[tuple[str, str], int],
    ):
        if t > max_t:
            return 0

        possible = {}
        time_left = max_t + 1 - t
        for valve in scan_map:
            if valve in opened or scan_map[valve].rate == 0:
                continue

            map_key = (min(valve, curr), max(valve, curr))
            traverse_time = traversal_map[map_key]
            released = (time_left - traverse_time - 1) * scan_map[valve].rate
            if released <= 0:
                continue

            possible[valve] = (released, traverse_time)

        if not possible:
            return 0

        possible_released = []
        for next_valve in possible:
            released, traverse_time = possible[next_valve]
            total_released = released + self.max_released(
                t + traverse_time + 1,
                max_t,
                next_valve,
                {**opened, next_valve: True},
                scan_map,
                traversal_map,
            )
            possible_released.append((next_valve, total_released))

        max_valve, max_released = max(possible_released, key=lambda kv: kv[1])
        return max_released

    def run_part_1(self, input) -> int:
        scans = self.parse_part_1(input)

        scan_map = {scan.name: scan for scan in scans}
        traversal_map = self.traverse(scan_map)
        return self.max_released(1, 30, "AA", {}, scan_map, traversal_map)

    def run_part_2(self, input) -> int:
        scans = self.parse_part_1(input)

        scan_map = {scan.name: scan for scan in scans}
        traversal_map = self.traverse(scan_map)
        relevant_valves = [scan.name for scan in scans if scan.rate > 0]
        relevant_valve_set = set(relevant_valves)

        splits = []
        for i in range(len(relevant_valves) // 2, len(relevant_valves) // 2 + 1):
            self_combs = itertools.combinations(relevant_valves, i)
            for combo in self_combs:
                combo_set = set(combo)
                eleph_set = relevant_valve_set.difference(combo_set)
                splits.append((combo_set, eleph_set))

        max_total_released = 0
        for i, (self_valves, eleph_valves) in enumerate(splits):
            self_scan_map = {
                valve: valve_scan
                for valve, valve_scan in scan_map.items()
                if valve in self_valves
            }
            self_max = self.max_released(1, 26, "AA", {}, self_scan_map, traversal_map)
            eleph_scan_map = {
                valve: valve_scan
                for valve, valve_scan in scan_map.items()
                if valve in eleph_valves
            }
            eleph_max = self.max_released(
                1, 26, "AA", {}, eleph_scan_map, traversal_map
            )
            total_released = self_max + eleph_max
            if total_released > max_total_released:
                max_total_released = total_released

        return max_total_released


class Day16Tests(AdventDayRunner, TestCase):
    instance_cls = Day16
