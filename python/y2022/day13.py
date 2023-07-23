from functools import cmp_to_key
from typing import Any

from shared import AdventDayV2


class Day13(AdventDayV2):
    def __init__(self):
        super(Day13, self).__init__()

    @staticmethod
    def compare(first, second) -> int:
        if type(first) != list and type(second) != list:
            if first < second:
                return -1
            elif first == second:
                return 0
            else:
                return 1

        if type(first) != list:
            first = [first]
        if type(second) != list:
            second = [second]

        for i in range(len(first)):
            if i >= len(second):
                return 1

            cmp = Day13.compare(first[i], second[i])
            if cmp == 1:
                return 1
            elif cmp == -1:
                return -1

        if len(first) < len(second):
            return -1
        else:
            return 0

    def parse_packet(self, line) -> list[Any]:
        inner = line[1:-1]

        elems = []
        tokens = []
        stack = 0
        for c in inner:
            if c == "[":
                stack += 1
            elif c == "]":
                stack -= 1

            if stack >= 1:
                tokens.append(c)
            else:
                if c == ",":
                    if stack == 0 and tokens:
                        elem = "".join(tokens)
                        elems.append(elem)
                        tokens = []
                else:
                    tokens.append(c)

        if tokens:
            elem = "".join(tokens)
            elems.append(elem)

        out: list[Any] = []
        for elem in elems:
            if elem[0] == "[":
                out.append(self.parse_packet(elem))
            else:
                out.append(int(elem))
        return out

    def run_part_1(self, input) -> int:
        pairs: list[list[str]] = []
        pair: list[str] = []
        for line in input:
            if not line.strip():
                pairs.append(pair)
                pair = []
            else:
                pair.append(line.strip())

        if pair:
            pairs.append(pair)

        total = 0
        for i, pair in enumerate(pairs):
            first_packet = self.parse_packet(pair[0])
            second_packet = self.parse_packet(pair[1])

            pair_idx = i + 1

            if self.compare(first_packet, second_packet) <= 0:
                total += pair_idx

        return total

    def run_part_2(self, input) -> int:
        divider_packets = [[[2]], [[6]]]
        packets = []
        for line in input:
            if line.strip():
                packet = self.parse_packet(line.strip())
                packets.append(packet)

        sorted_packets = sorted(
            packets + divider_packets, key=cmp_to_key(Day13.compare)
        )
        divider_idxs = [
            (sorted_packets.index(divider_packet) + 1)
            for divider_packet in divider_packets
        ]
        return divider_idxs[0] * divider_idxs[1]


class Day13Tests(AdventDayV2.Tests):
    instance_cls = Day13
    EXPECTED = {
        (1, True): 13,
        (1, False): 5390,
        (2, True): 140,
        (2, False): 19261,
    }
