import copy
from numpy import sign

from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        data.packet_pairs = [(eval(pair.splitlines()[0]), eval(pair.splitlines()[1])) for pair in text.split("\n\n")]

    def compute(self, data):
        return sum(index + 1 if self.compare_lists(packet1, packet2) == -1 else 0
                   for index, (packet1, packet2) in enumerate(data.packet_pairs))

    @staticmethod
    def compare_lists(list1, list2):
        while 1:
            if len(list1) == 0 and len(list2) == 0:
                return 0
            if len(list1) == 0:
                return -1
            if len(list2) == 0:
                return 1
            data1 = list1.pop(0)
            data2 = list2.pop(0)
            result = PartA.compare(data1, data2)
            if result != 0:
                return result

    @staticmethod
    def compare(data1, data2):
        if type(data1) == list and type(data2) == list:
            return PartA.compare_lists(data1, data2)
        if type(data1) == int and type(data2) == int:
            return sign(data1 - data2)
        if type(data1) != list:
            data1 = [data1]
        if type(data2) != list:
            data2 = [data2]
        return PartA.compare_lists(data1, data2)


class PartB(PartA):
    def compute(self, data):
        packets = [item for pair in data.packet_pairs for item in pair]
        sorted_packets = [[[2]], [[6]]]
        while len(packets) > 0:
            packet = packets.pop(0)
            for i in range(len(sorted_packets)):
                if PartA.compare_lists(copy.deepcopy(packet), copy.deepcopy(sorted_packets[i])) == -1:
                    sorted_packets.insert(i, packet)
                    packet = None
                    break
            if packet:
                sorted_packets.append(packet)

        marker1 = sorted_packets.index([[2]]) + 1
        marker2 = sorted_packets.index([[6]]) + 1
        return marker1 * marker2


Day.do_day(13, 2022, PartA, PartB)
