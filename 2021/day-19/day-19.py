import os
from collections import defaultdict, namedtuple
from itertools import combinations, product
from math import sqrt
from typing import List, Tuple


def read_input_from_file(file_name: str) -> dict:
    script_path = os.path.dirname(os.path.abspath(__file__))
    input_file = open(f"{script_path}/{file_name}", "r")
    groups = input_file.read().strip().split("\n\n")
    input_file.close()

    scanners = {}
    for i, group in enumerate(groups):
        scanners[i] = [tuple(map(int, line.split(","))) for line in group.split("\n")[1:]]
    return scanners


rotations = [([2, 0, 1], [-1, -1, 1]),  ([0, 1, 2], [1, -1, -1]),
             ([2, 1, 0], [-1, -1, -1]), ([2, 1, 0], [1, -1, 1]),
             ([0, 1, 2], [1, 1, 1]),    ([1, 0, 2], [1, -1, 1]),
             ([1, 0, 2], [-1, 1, 1]),   ([0, 1, 2], [-1, -1, 1]),
             ([0, 2, 1], [-1, -1, -1]), ([1, 2, 0], [1, -1, -1]),
             ([1, 0, 2], [-1, -1, -1]), ([1, 2, 0], [1, 1, 1]),
             ([1, 0, 2], [1, 1, -1]),   ([2, 1, 0], [1, 1, -1]),
             ([2, 0, 1], [1, 1, 1]),    ([2, 1, 0], [-1, 1, 1]),
             ([0, 2, 1], [-1, 1, 1]),   ([0, 1, 2], [-1, 1, -1]),
             ([0, 2, 1], [1, -1, 1]),   ([2, 0, 1], [-1, 1, -1]),
             ([1, 2, 0], [-1, 1, -1]),  ([1, 2, 0], [-1, -1, 1]),
             ([0, 2, 1], [1, 1, -1]),   ([2, 0, 1], [1, -1, -1])]


Point3 = namedtuple('Point', 'x y z')


def part_a(scanners) -> Tuple[int, List[List[int]]]:
    intersects = get_intersections(scanners)
    mapping_dict = generate_mappings(intersects, scanners)
    beacons = set(to_point(p) for p in scanners[0])
    used_mappings = set()
    transformed_scanners = {0}
    scanner_origins = [[0] * 3]
    while len(transformed_scanners) < len(scanners):
        queue = [k for k in mapping_dict.keys()
                 if k[0] in transformed_scanners and k[1] not in transformed_scanners]
        while len(queue) > 0:
            intersect = queue.pop()
            if intersect[1] in transformed_scanners:
                continue
            p_transpose = list(zip(*scanners[intersect[1]]))
            centroid = list(zip([0, 0, 0]))
            use_mapping = intersect
            while True:
                centroid = transform(centroid, *mapping_dict[use_mapping])
                p_transpose = transform(p_transpose, *mapping_dict[use_mapping])
                new_points = set(to_point(p) for p in zip(*p_transpose))
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
    return len(beacons), scanner_origins


def find_max_distance(scanner_origins: List) -> int:
    return max(sum(map(lambda x: abs(x[0] - x[1]), zip(*p))) for p in combinations(scanner_origins, 2))


def generate_mappings(intersects, scanners):
    mapping_dict = {}
    for i in intersects:
        p2dist_a = defaultdict(set)
        for p in combinations(scanners[i[0]], 2):
            dist = euclid_distance(*p)
            p2dist_a[to_point(p[0])].add(dist)
            p2dist_a[to_point(p[1])].add(dist)
        p2dist_b = defaultdict(set)
        for p in combinations(scanners[i[1]], 2):
            dist = euclid_distance(*p)
            p2dist_b[to_point(p[0])].add(dist)
            p2dist_b[to_point(p[1])].add(dist)
        points_a = []
        points_b = []
        for p in product(p2dist_a.keys(), p2dist_b.keys()):
            intersect = p2dist_a[p[0]].intersection(p2dist_b[p[1]])
            if len(intersect) >= 11:
                points_a.append(point_to_list(p[0]))
                points_b.append(point_to_list(p[1]))
        mapping_dict[i] = map_scanner_a_to_b(points_a, points_b)
    return mapping_dict


def map_scanner_a_to_b(points_a, points_b):
    a_transpose = list(zip(*points_a))
    b_transpose = list(zip(*points_b))
    for perms, signs in rotations:
        rotated = rotate(b_transpose, perms, signs)
        offset = []
        for p in zip(rotated, a_transpose):
            points = set([x[1] - x[0] for x in zip(p[0], p[1])])
            if len(points) == 1:
                offset.append(points.pop())
            if len(offset) == 3:
                return offset, perms, signs
    return None


def transform(to_transform, target_center, trans_perm, trans_sign):
    rotated = rotate(to_transform, trans_perm, trans_sign)
    return [list(map(lambda x: target_center[i] + x, p)) for i, p in enumerate(rotated)]


def get_intersections(scanners):
    intersections = []
    distance_dict = {i: set(euclid_distance(*p) for p in combinations(scanners[i], 2)) for i in scanners.keys()}
    for i in combinations(range(len(scanners)), 2):
        if len(distance_dict[i[0]].intersection(distance_dict[i[1]])) >= 66:  # 12!/10! / 2
            intersections.append(i)
            intersections.append(i[::-1])
    return intersections


def rotate(point, perms, signs):
    return map(lambda n: n * signs[0], point[perms[0]]), \
           map(lambda n: n * signs[1], point[perms[1]]), \
           map(lambda n: n * signs[2], point[perms[2]])


def euclid_distance(a, b):
    return sqrt(sum(map(lambda x: pow(x[0] - x[1], 2), zip(a, b))))


def to_point(plist):
    if len(plist) == 3:
        return Point3(plist[0], plist[1], plist[2])
    else:
        raise Exception("Need 3 values for a point")


def point_to_list(p):
    return [p.x, p.y, p.z]


def main() -> None:
    example_data = read_input_from_file("example.txt")
    data = read_input_from_file("input.txt")

    num_beacons, origins = part_a(data)
    max_dist = find_max_distance(origins)
    print(f"Part 1 beacons: {num_beacons}")
    print(f"Part 2 max distance: {max_dist}")

    part_a(example_data)
    part_a(data)


if __name__ == "__main__":
    main()
