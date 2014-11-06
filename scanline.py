#!/usr/bin/env python

import sys
from bbstree import BalancedBinarySearchTree
from precision import FloatingPoint

debug = False

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


class VisibleTip:
    def __init__(self, eventType, point):
        self.point = point
        self.eventType = eventType
        self.index = point.index

    def __repr__(self):
        if self.eventType == "start":
            return "[" + str(self.point)    
        else:
            return str(self.point) + "]"


class VisibleSegments:
    def __init__(self, results):
        self.results = results

    def openVisibleInterval(self, point):
        if debug: print "Opening visibility of segment " + str(point.index)
        self.results[point.index].append(VisibleTip("start", point))

    def closeVisibleInterval(self, point):
        if debug: print "Closing visibility of segment " + str(point.index)
        self.results[point.index].append(VisibleTip("end", point))

    def __repr__(self):
        res = ""
        i = 0
        for entry in self.results:
            middle = ""
            for tip in entry:
                middle = middle + str(tip) + " ; "

            res = res + str(i) + ": "
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


def intersect(p1, p2, p3, p4):
    x1 = p1.x
    x2 = p2.x
    x3 = p3.x
    x4 = p4.x
    y1 = p1.y
    y2 = p2.y
    y3 = p3.y
    y4 = p4.y

    q_x = ((((x1*y2) - (y1*x2))*(x3-x4)) - ((x1-x2)*((x3*y4) - (y3*x4))))/(((x1 - x2)*(y3 - y4)) - ((y1 - y2)*(x3 - x4)))
    q_y = ((((x1*y2) - (y1*x2))*(y3-y4)) - ((y1-y2)*((x3*y4) - (y3*x4))))/(((x1 - x2)*(y3 - y4)) - ((y1 - y2)*(x3 - x4)))
    return Point(q_x, q_y)


# Determines the visibility of a segment based on the case.
def determine_visibility(case, current, last, just_treated, results):
    if last == None:
        results.openVisibleInterval(current.left_extreme)
        return
    
    if current == None:
        results.closeVisibleInterval(last.right_extreme)
        return

    if current.index == just_treated:
        if case == "insertion":
            p = intersect(last.left_extreme, last.right_extreme, LineSegment.origin, current.left_extreme)
            p.set_segment_index(last.index)
            results.closeVisibleInterval(p)
            results.openVisibleInterval(current.left_extreme)
            return
    else:
        if (not current == last) and case == "remotion":
            results.closeVisibleInterval(last.right_extreme)
            p = intersect(current.left_extreme, current.right_extreme, LineSegment.origin, last.right_extreme)
            p.set_segment_index(current.index)
            results.openVisibleInterval(p)
            return


# Scan line algorithm
def scan_line_radar(segments, extremes):
    sorted_extremes = sorted(extremes, cmp=compare_polar_angles)
    scan_line = build_initial_tree(segments, sorted_extremes)


    results = [[] for each_element in segments]
    result = VisibleSegments(results)
    last_visible = None 

    if debug: 
        for p in sorted_extremes:
            print p.index

    initial_point = None
    current_visible = scan_line.min()
    if not (current_visible is None):
        p_aux = Point(LineSegment.origin.x + 1, LineSegment.origin.y)
        initial_point = intersect(current_visible.left_extreme, current_visible.right_extreme, LineSegment.origin, p_aux)
        initial_point.set_segment_index(current_visible.index)
        result.openVisibleInterval(initial_point)
        last_visible = current_visible

    for point in sorted_extremes:
        if point.is_left_extreme:
            scan_line.insert(segments[point.index])
            case = "insertion"
        else:
            scan_line.remove(segments[point.index])
            case = "remotion"

        current_visible = scan_line.min()
        
        if debug:
            print "case: " + case
            print "iteration point: " + str(point.index) + "        -      " + str(point)
            print "current visible: ",
            if current_visible: print str(current_visible.index)
            else: print "None"

        determine_visibility(case, current_visible, last_visible, point.index, result)

        if debug: print "\n"

        last_visible = current_visible

    if not (initial_point is None):
        result.closeVisibleInterval(initial_point)

    return result


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


print 'Visible segments from',
print guard
guarded_walls = scan_line_radar(segments, extremes)
print "\n" + str(guarded_walls)
