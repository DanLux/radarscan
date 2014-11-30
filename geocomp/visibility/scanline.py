#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from bbstree import BalancedBinarySearchTree
from graphic import GraphicAnimation
from geometry import Point
from geometry import LineSegment


debug = False

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


class VisibleSegments:
    def __init__(self, visible_sections):
        self.visible_sections = visible_sections
        self.visible_segments = []

    def openVisibleInterval(self, point):
        if debug: print 'Opening visibility of segment ' + str(point.index)
        self.visible_sections[point.index].append(point)
        self.visible_segments.append(point)

    def closeVisibleInterval(self, point):
        if debug: print 'Closing visibility of segment ' + str(point.index)
        self.visible_sections[point.index].append(point)
        self.visible_segments.append(point)

    def __repr__(self):
        res = ''
        i = 0
        for entry in self.visible_sections:
            middle = ''
            for k in range(0, len(entry), 2):
                middle += '[' + str(entry[k]) + '; ' + str(entry[k + 1]) + ']; '

            res = res + str(i) + ': '
            res = res + middle + '\n'
            i = i + 1
        return res



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


def intersection_point(p1, p2, p3, p4):
    x = ((((p1.x*p2.y) - (p1.y*p2.x))*(p3.x-p4.x)) - ((p1.x-p2.x)*((p3.x*p4.y) - (p3.y*p4.x))))/ \
            (((p1.x - p2.x)*(p3.y - p4.y)) - ((p1.y - p2.y)*(p3.x - p4.x)))
    y = ((((p1.x*p2.y) - (p1.y*p2.x))*(p3.y-p4.y)) - ((p1.y-p2.y)*((p3.x*p4.y) - (p3.y*p4.x))))/ \
            (((p1.x - p2.x)*(p3.y - p4.y)) - ((p1.y - p2.y)*(p3.x - p4.x)))
    return Point(x, y)


# Determines the visibility of a segment based on the case.
def determine_visibility(case, current, last, just_treated, results):
    if last == None:
        results.openVisibleInterval(current.left_extreme)

    elif current == None:
        results.closeVisibleInterval(last.right_extreme)

    elif current.index == just_treated:
        if case == 'insertion':
            p = intersection_point(last.left_extreme, last.right_extreme, LineSegment.origin, current.left_extreme)
            p.set_segment_index(last.index)
            results.closeVisibleInterval(p)
            results.openVisibleInterval(current.left_extreme)

    else:
        if (not current == last) and case == 'remotion':
            results.closeVisibleInterval(last.right_extreme)
            p = intersection_point(current.left_extreme, current.right_extreme, LineSegment.origin, last.right_extreme)
            p.set_segment_index(current.index)
            results.openVisibleInterval(p)


# Scan line algorithm
def scan_line_radar(segments, extremes):
    sorted_extremes = sorted(extremes, cmp=compare_polar_angles)
    scan_line = build_initial_tree(segments, sorted_extremes)

    results = [[] for each_element in segments]
    result = VisibleSegments(results)
    last_visible = None

    if debug:
        for p in sorted_extremes: print p.index

    initial_point = None
    current_visible = scan_line.min()
    if not (current_visible is None):
        p_aux = Point(LineSegment.origin.x + 1, LineSegment.origin.y)
        initial_point = intersection_point(current_visible.left_extreme, current_visible.right_extreme, LineSegment.origin, p_aux)
        initial_point.set_segment_index(current_visible.index)
        result.openVisibleInterval(initial_point)
        last_visible = current_visible

    for point in sorted_extremes:
        if point.is_left_extreme:
            scan_line.insert(segments[point.index])
            case = 'insertion'
        else:
            scan_line.remove(segments[point.index])
            case = 'remotion'

        current_visible = scan_line.min()

        if debug:
            print 'case: ' + case
            print 'iteration point: ' + str(point.index) + ' - ' + str(point)
            print 'current visible: ',
            if current_visible: print str(current_visible.index)
            else: print 'None'

        determine_visibility(case, current_visible, last_visible, point.index, result)

        if debug: print '\n'

        last_visible = current_visible

    if not (initial_point is None):
        result.closeVisibleInterval(initial_point)

    return result


def build_data_structures(entry):
    x, y = entry.pop(0)
    guard = Point(x, y)
    LineSegment.set_origin(guard)

    extremes = []
    segments = []
    while len(entry) > 0:
        x, y = entry.pop(0)
        p = Point(x, y)

        x, y = entry.pop(0)
        q = Point(x, y)

        k = len(segments)
        p.set_segment_index(k)
        q.set_segment_index(k)
        segments.append(LineSegment(p, q))
        extremes.append(p)
        extremes.append(q)
    return (extremes, segments)


# Algorithm called by the graphical interface
def radar_scan(input_list):
    entry = [ (input_list[0].x, input_list[0].y) ]
    for segment in input_list[1:]:
        entry.append((segment.init.x, segment.init.y))
        entry.append((segment.to.x, segment.to.y))

    extremes, segments = build_data_structures(entry)

    guarded_walls = scan_line_radar(segments, extremes).visible_segments
    print guarded_walls
    GraphicAnimation(LineSegment.origin, guarded_walls).draw_animation()


# Solves the problem when entry is read from standard output
def main():
    input_list = sys.stdin.read().split()
    if len(input_list) % 4 != 2:
        raise Exception('Invalid input')

    entry = []
    while len(input_list) > 0:
        entry.append((input_list.pop(0), input_list.pop(0)))

    extremes, segments = build_data_structures(entry)

    guard = LineSegment.origin
    print 'Visible segments from', guard, '\n'
    guarded_walls = scan_line_radar(segments, extremes)
    print guarded_walls