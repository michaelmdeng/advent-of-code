from collections import deque, namedtuple
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
            if valve in searched:
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
        curr: str,
        opened: dict[str, bool],
        scan_map: dict[str, ValveScan],
        traversal_map: dict[tuple[str, str], int],
    ):
        if t > 30:
            return 0

        possible = {}
        time_left = 31 - t
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
        return self.max_released(1, "AA", {}, scan_map, traversal_map)

    def run_part_2(self, input) -> None:
        pass


class Day16Tests(AdventDayRunner, TestCase):
    instance_cls = Day16
