#!/usr/bin/env python

import sys
from bbstree import BalancedBinarySearchTree
from precision import FloatingPoint


class Point:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return repr((self.x, self.y))

    def set_left_extreme(self, extreme):
        self.is_left_extreme = extreme

    def set_segment_index(self, index):
        self.index = index

    def equals(self, point):
        return FloatingPoint.is_zero(self.x - point.x) and \
                FloatingPoint.is_zero(self.y - point.y)

    def relative_quadrant(self, origin):
        p = self.__translate(origin)
        if p.x >= 0 and p.y >= 0: return 1
        elif p.x <= 0 and p.y >= 0: return 2
        elif p.x <= 0 and p.y <= 0: return 3
        else: return 4

    def area(self, point1, point2):
        return (point1.x - self.x) * (point2.y - self.y) - \
               (point1.y - self.y) * (point2.x - self.x)

    def colinear(self, point1, point2):
        return FloatingPoint.is_zero(self.area(point1, point2))

    def on_the_left_side(self, left_extreme, right_extreme):
        return self.area(left_extreme, right_extreme) > 0

    def strictly_in_line_segment(self, point1, point2):
        if not self.colinear(point1, point2): return False

        if point1.x != point2.x:
            return (point1.x < self.x < point2.x) or \
                   (point2.x < self.x < point1.x)
        else:
            return (point1.y < self.y < point2.y) or \
                   (point2.y < self.y < point1.y)

    def __translate(self, origin):
        return Point(self.x - origin.x, self.y - origin.y)


class LineSegment:
    origin = None

    def __init__(self, p, q):
        if LineSegment.origin is None:
            raise Exception('Must call static method set_origin first')

        if LineSegment.origin.on_the_left_side(p, q):
            self.__set_segment(p, q)
        else: self.__set_segment(q, p)
        self.index = p.index

    def __repr__(self):
        return '[' + repr(self.left_extreme) + '; ' + repr(self.right_extreme) + ']'

    def equals(self, segment):
        p = self.left_extreme
        q = self.right_extreme
        r = segment.left_extreme
        s = segment.right_extreme
        return p.equals(r) and q.equals(s)

    def __set_segment(self, left_extreme, right_extreme):
        left_extreme.set_left_extreme(True)
        self.left_extreme = left_extreme
        right_extreme.set_left_extreme(False)
        self.right_extreme = right_extreme

    @staticmethod
    def set_origin(origin):
        LineSegment.origin = origin



class LineSegmentBalancedTree(BalancedBinarySearchTree):
    @staticmethod
    def points_comparison_function(self, node):
        if self.value.equals(node.value): return 0
        p = self.value.left_extreme
        q = node.value.left_extreme

        # self and node are both in the scanline
        if p.strictly_in_line_segment(LineSegment.origin, q):
            return -1 # self < node
        elif q.strictly_in_line_segment(LineSegment.origin, p):
            return 1
        else:
            if q.on_the_left_side(LineSegment.origin, p):
                if q.on_the_left_side(p, self.value.right_extreme):
                    return 1
                else: return -1
            else:
                if p.on_the_left_side(q, node.value.right_extreme):
                    return -1
                else: return 1

    def __init__(self):
        BalancedBinarySearchTree.__init__(self, LineSegmentBalancedTree.points_comparison_function)



def compare_polar_angles(point1, point2):
    origin = LineSegment.origin
    point1_quadrant = point1.relative_quadrant(origin)
    point2_quadrant = point2.relative_quadrant(origin)
    if point1_quadrant != point2_quadrant:
        if point1_quadrant < point2_quadrant: return -1
        else: return 1
    else:
        if point1.strictly_in_line_segment(origin, point2):
            if not point1.is_left_extreme:
                return 1
            else: return -1
        elif point2.strictly_in_line_segment(origin, point1):
            if not point2.is_left_extreme:
                return -1
            else: return 1
        else:
            if point1.on_the_left_side(origin, point2): return 1
            else: return -1


def build_initial_tree(segments, sorted_extremes):
    is_initial_segment = [True for each_element in segments]
    for extreme in sorted_extremes:
        if extreme.is_left_extreme:
            is_initial_segment[extreme.index] = not is_initial_segment[extreme.index]
        else: is_initial_segment[extreme.index] = False
    initial_segments = [ segments[index] for index, present in
                        enumerate(is_initial_segment) if present  ]

    tree = LineSegmentBalancedTree()
    for segment in initial_segments: tree.insert(segment)
    return tree


# Scan line algorithm
def scan_line_radar(segments, extremes):
    sorted_extremes = sorted(extremes, cmp=compare_polar_angles)
    scan_line = build_initial_tree(segments, sorted_extremes)

    is_visible_segment = [False for each_element in segments]
    visible = scan_line.min()
    if not (visible is None):
        is_visible_segment[visible.index] = True

    for point in sorted_extremes:
        if point.is_left_extreme:
            scan_line.insert(segments[point.index])
        else:
            scan_line.remove(segments[point.index])
        visible = scan_line.min()
        if not (visible is None):
            is_visible_segment[visible.index] = True

    return [ segments[index] for index, present in
            enumerate(is_visible_segment) if present ]



# Main program
entry = sys.stdin.read().split()
if len(entry) % 4 != 2:
    raise Exception("Invalid input")

# Reading input
guard = Point(entry.pop(0), entry.pop(0))
LineSegment.set_origin(guard)
extremes = []
segments = []
while len(entry) > 0:
    x = entry.pop(0)
    y = entry.pop(0)
    p = Point(x, y)

    x = entry.pop(0)
    y = entry.pop(0)
    q = Point(x, y)

    k = len(segments)
    p.set_segment_index(k)
    q.set_segment_index(k)
    segments.append(LineSegment(p, q))
    extremes.append(p)
    extremes.append(q)


guarded_walls = scan_line_radar(segments, extremes)
print 'Visible segments from',
print guard
for wall in guarded_walls:
    print wall
