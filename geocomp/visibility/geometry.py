#!/usr/bin/env python
# -*- coding: utf-8 -*-

from precision import FloatingPoint
from geocomp.common import point


class Point(point.Point):
    def __init__(self, x, y):
        point.Point.__init__(self, float(x), float(y))

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