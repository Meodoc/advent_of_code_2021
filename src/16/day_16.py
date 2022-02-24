from aocd.models import Puzzle
from math import ceil, prod


class Packet:
    def __init__(self, version: int, type_id: int, length: int):
        self.version = version
        self.type_id = type_id
        self.length = length
        self.value = ValueError()

    def sum_version_numbers(self) -> int:
        raise NotImplementedError()


class LiteralPacket(Packet):
    def __init__(self, version: int, type_id: int, length: int, value: int):
        super().__init__(version, type_id, length)
        self.value = value

    def sum_version_numbers(self) -> int:
        return self.version


class OperatorPacket(Packet):
    def __init__(self, version: int, type_id: int, length: int, sub_packets: list):
        super().__init__(version, type_id, length)
        self.sub_packets = sub_packets
        self.value = self._calculate_value()

    def sum_version_numbers(self) -> int:
        sum_ = self.version
        for sub_packet in self.sub_packets:
            sum_ += sub_packet.sum_version_numbers()
        return sum_

    def _calculate_value(self) -> int:
        if self.type_id == 0:
            return sum(sub_packet.value for sub_packet in self.sub_packets)
        if self.type_id == 1:
            return prod(sub_packet.value for sub_packet in self.sub_packets)
        if self.type_id == 2:
            return min(sub_packet.value for sub_packet in self.sub_packets)
        if self.type_id == 3:
            return max(sub_packet.value for sub_packet in self.sub_packets)
        if self.type_id == 5:
            assert (len(self.sub_packets) == 2)
            return 1 if self.sub_packets[0].value > self.sub_packets[1].value else 0
        if self.type_id == 6:
            assert (len(self.sub_packets) == 2)
            return 1 if self.sub_packets[0].value < self.sub_packets[1].value else 0
        if self.type_id == 7:
            assert (len(self.sub_packets) == 2)
            return 1 if self.sub_packets[0].value == self.sub_packets[1].value else 0


def part_a(packet: Packet):
    return packet.sum_version_numbers()


def part_b(packet: Packet):
    return packet.value


def parse(data: str):
    def parse_literal():
        literal = data[6:]

        # pad literal to next bigger multiple length of 4
        padded_literal_len = 4 * ceil(len(literal) / 4)
        literal = literal + '0' * (padded_literal_len - len(literal))

        # extract the literal value
        lit_val = ''
        consumed_len = 6
        for i in range(0, padded_literal_len - 5, 5):
            group_header = int(literal[i])
            lit_val += literal[i + 1: i + 5]
            if group_header == 0:
                consumed_len += i + 5
                break

        lit_val = int(lit_val, 2)

        return LiteralPacket(version, type_id, consumed_len, lit_val)

    def parse_operator():
        length_type_id = int(data[6])

        if length_type_id == 0:
            expected_sub_len = int(data[7:22], 2)
            total_sub_len = 0
            sub_packets = []
            while total_sub_len < expected_sub_len:
                sub = parse(data[22 + total_sub_len:])
                sub_packets.append(sub)
                total_sub_len += sub.length

            assert (total_sub_len == expected_sub_len)

            consumed_len = 22 + total_sub_len
            return OperatorPacket(version, type_id, consumed_len, sub_packets)

        elif length_type_id == 1:
            n_sub_packets = int(data[7:18], 2)
            total_sub_len = 0
            sub_packets = []
            for _ in range(n_sub_packets):
                sub = parse(data[18 + total_sub_len:])
                sub_packets.append(sub)
                total_sub_len += sub.length

            consumed_len = 18 + total_sub_len
            return OperatorPacket(version, type_id, consumed_len, sub_packets)

    version = int(data[0:3], 2)
    type_id = int(data[3:6], 2)

    if type_id == 4:
        return parse_literal()
    else:
        return parse_operator()


def load(data: str):
    bin_len = len(data) * 4
    data = int(data, 16)
    data = format(data, f'0{bin_len}b')
    return parse(data)


puzzle = Puzzle(year=2021, day=16)
ans_a = part_a(load(puzzle.input_data))
# puzzle.answer_a = ans_a  # 984

ans_b = part_b(load(puzzle.input_data))
# puzzle.answer_b = ans_b  # 1015320896946
