import functools
import operator
from mylib.aoc_basics import Day


class Packet:
    def __init__(self, version, packet_type, length, data) -> None:
        self.version = version
        self.type = packet_type
        self.length = length
        self.data = data

    def value(self):
        match self.type:
            case 0: return sum(sub.value() for sub in self.data)
            case 1: return functools.reduce(operator.mul, [sub.value() for sub in self.data])
            case 2: return min(sub.value() for sub in self.data)
            case 3: return max(sub.value() for sub in self.data)
            case 4: return self.data
            case 5: return 1 if self.data[0].value() > self.data[1].value() else 0
            case 6: return 1 if self.data[0].value() < self.data[1].value() else 0
            case 7: return 1 if self.data[0].value() == self.data[1].value() else 0
            case _: raise RuntimeError("Illegal Packet Type")

    def version_sum(self):
        if self.type == 4:
            return self.version
        return self.version + sum(sb.version_sum() for sb in self.data)

    @classmethod
    def from_string(cls, text):
        version = int(text[0:3], 2)
        packet_type = int(text[3:6], 2)
        content = text[6:]

        if packet_type == 4:
            data, length = cls.parse_literal_value(content)
        else:
            data, length = cls.parse_subpackets(content)

        return cls(version, packet_type, length + 6, data)

    @staticmethod
    def parse_literal_value(text):
        value = ""
        length = 0
        while True:
            value += text[1:5]
            length += 5
            if text[0] == "0":
                break
            text = text[5:]
        return int(value, 2), length

    @classmethod
    def parse_subpackets(cls, text):
        length = 1
        length_type = text[0]
        current_length = 0
        subpackets = []
        if length_type == "0":
            subpacket_length = int(text[1:16], 2)
            text = text[16:]
            length += 15
        else:
            subpacket_length = int(text[1:12], 2)
            text = text[12:]
            length += 11
        while current_length < subpacket_length:
            subpacket = Packet.from_string(text)
            subpackets.append(subpacket)
            length += subpacket.length
            text = text[subpacket.length:]
            current_length += 1 if length_type == "1" else subpacket.length
        return subpackets, length


class PartA(Day):
    def parse(self, text, data):
        binary_text = "".join(f"{int(c, 16):04b}" for c in text)
        data.packet = Packet.from_string(binary_text)

    def compute(self, data):
        return data.packet.version_sum()

    def example_answer(self):
        return 16

    def get_example_input(self, puzzle):
        return "8A004A801A8002F478"

    def tests(self):
        yield "620080001611562C8802118E34", 12, "Operator Packet with 2 subpackets"
        yield "C0015000016115A2E0802F182340", 23, "Operator Packet with length type 1"
        yield "A0016C880162017C3686B18A3D4780", 31, "Multiple nested packets"


class PartB(PartA):
    def compute(self, data):
        return data.packet.value()

    def example_answer(self):
        return 15

    def tests(self):
        yield "C200B40A82", 3, "Sum of 1 and 2"
        yield "04005AC33890", 54, "Product of 6 and 9"
        yield "880086C3E88112", 7, "Min of 7, 8 and 9"
        yield "CE00C43D881120", 9, "Max of 7, 8, and 9"
        yield "D8005AC2A8F0", 1, "5 less than 15"
        yield "F600BC2D8F", 0, "5 greater than 15"
        yield "9C005AC2F8F0", 0, "5 equal to 15"
        yield "9C0141080250320F1802104A08", 1, "1 + 3 = 2 * 2"


Day.do_day(16, 2021, PartA, PartB)
