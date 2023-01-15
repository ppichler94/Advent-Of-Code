import re
from collections import defaultdict
from itertools import combinations, product
from math import sqrt
from typing import List
from mylib.aoc_basics import Day


class PartA(Day):
    def parse(self, text, data):
        groups = text.split("\n\n")
        data.scanners = {i: [tuple(map(int, re.findall(r"-?\d+", line)))
                             for line in group.splitlines()[1:]]
                         for i, group in enumerate(groups)}
        data.rotations = [([2, 0, 1], [-1, -1, 1]), ([0, 1, 2], [1, -1, -1]),
                          ([2, 1, 0], [-1, -1, -1]), ([2, 1, 0], [1, -1, 1]),
                          ([0, 1, 2], [1, 1, 1]), ([1, 0, 2], [1, -1, 1]),
                          ([1, 0, 2], [-1, 1, 1]), ([0, 1, 2], [-1, -1, 1]),
                          ([0, 2, 1], [-1, -1, -1]), ([1, 2, 0], [1, -1, -1]),
                          ([1, 0, 2], [-1, -1, -1]), ([1, 2, 0], [1, 1, 1]),
                          ([1, 0, 2], [1, 1, -1]), ([2, 1, 0], [1, 1, -1]),
                          ([2, 0, 1], [1, 1, 1]), ([2, 1, 0], [-1, 1, 1]),
                          ([0, 2, 1], [-1, 1, 1]), ([0, 1, 2], [-1, 1, -1]),
                          ([0, 2, 1], [1, -1, 1]), ([2, 0, 1], [-1, 1, -1]),
                          ([1, 2, 0], [-1, 1, -1]), ([1, 2, 0], [-1, -1, 1]),
                          ([0, 2, 1], [1, 1, -1]), ([2, 0, 1], [1, -1, -1])]

    def compute(self, data):
        beacons, _ = self.find_beacons(data)
        return len(beacons)

    def find_beacons(self, data):
        intersects = self.get_intersections(data.scanners)
        mapping_dict = self.generate_mappings(intersects, data)
        beacons = set(p for p in data.scanners[0])
        used_mappings = set()
        transformed_scanners = {0}
        scanner_origins = [[0] * 3]
        while len(transformed_scanners) < len(data.scanners):
            queue = [k for k in mapping_dict.keys()
                     if k[0] in transformed_scanners and k[1] not in transformed_scanners]
            while len(queue) > 0:
                intersect = queue.pop()
                if intersect[1] in transformed_scanners:
                    continue
                p_transpose = list(zip(*data.scanners[intersect[1]]))
                centroid = list(zip([0, 0, 0]))
                use_mapping = intersect
                while True:
                    centroid = transform(centroid, *mapping_dict[use_mapping])
                    p_transpose = transform(p_transpose, *mapping_dict[use_mapping])
                    new_points = set(p for p in zip(*p_transpose))
                    if use_mapping[0] == 0:
                        break
                    for mapping in used_mappings:
                        if mapping[1] == use_mapping[0]:
                            use_mapping = mapping
                            break
                scanner_origins.append([centroid[0][0], centroid[1][0], centroid[2][0]])
                transformed_scanners.add(intersect[1])
                beacons.update(new_points)
                used_mappings.add(intersect)
        return beacons, scanner_origins

    @staticmethod
    def get_intersections(scanners):
        intersections = []
        distance_dict = {i: set(euclid_distance(*p) for p in combinations(scanners[i], 2)) for i in
                         scanners.keys()}
        for i in combinations(range(len(scanners)), 2):
            if len(distance_dict[i[0]].intersection(distance_dict[i[1]])) >= 66:  # 12!/10! / 2
                intersections.append(i)
                intersections.append(i[::-1])
        return intersections

    def generate_mappings(self, intersects, data):
        mapping_dict = {}
        for i in intersects:
            p2dist_a = defaultdict(set)
            for p in combinations(data.scanners[i[0]], 2):
                dist = euclid_distance(*p)
                p2dist_a[p[0]].add(dist)
                p2dist_a[p[1]].add(dist)
            p2dist_b = defaultdict(set)
            for p in combinations(data.scanners[i[1]], 2):
                dist = euclid_distance(*p)
                p2dist_b[p[0]].add(dist)
                p2dist_b[p[1]].add(dist)
            points_a = []
            points_b = []
            for p in product(p2dist_a.keys(), p2dist_b.keys()):
                intersect = p2dist_a[p[0]].intersection(p2dist_b[p[1]])
                if len(intersect) >= 11:
                    points_a.append(p[0])
                    points_b.append(p[1])
            mapping_dict[i] = self.map_scanner_a_to_b(data, points_a, points_b)
        return mapping_dict

    @staticmethod
    def map_scanner_a_to_b(data, points_a, points_b):
        a_transpose = list(zip(*points_a))
        b_transpose = list(zip(*points_b))
        for perms, signs in data.rotations:
            rotated = rotate(b_transpose, perms, signs)
            offset = []
            for p in zip(rotated, a_transpose):
                points = set([x[1] - x[0] for x in zip(p[0], p[1])])
                if len(points) == 1:
                    offset.append(points.pop())
                if len(offset) == 3:
                    return offset, perms, signs
        return None

    def example_answer(self):
        return 79

    def get_example_input(self, puzzle):
        return """
--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14        
"""


class PartB(PartA):
    def compute(self, data):
        _, origins = self.find_beacons(data)
        return max(sum(map(lambda x: abs(x[0] - x[1]), zip(*p))) for p in combinations(origins, 2))

    def example_answer(self):
        return 3621


def euclid_distance(a, b):
    return sqrt(sum(map(lambda x: pow(x[0] - x[1], 2), zip(a, b))))


def transform(to_transform, target_center, trans_perm, trans_sign):
    rotated = rotate(to_transform, trans_perm, trans_sign)
    return [list(map(lambda x, i=i: target_center[i] + x, p)) for i, p in enumerate(rotated)]


def rotate(point, perms, signs):
    return map(lambda n: n * signs[0], point[perms[0]]), \
        map(lambda n: n * signs[1], point[perms[1]]), \
        map(lambda n: n * signs[2], point[perms[2]])


Day.do_day(19, 2021, PartA, PartB)
