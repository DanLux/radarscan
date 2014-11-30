# -*- coding: utf-8 -*-

from geocomp.common import control
from geocomp import config

class GraphicAnimation:
    def __init__(self, origin, points_list):
        self.origin = origin
        self.points = points_list

    def update(self):
        control.thaw_update()
        control.update()
        control.freeze_update()
        control.sleep()

    def draw_line(self, point1, point2, color):
        point1.lineto(point2, color)
        self.update()

    def erase_line(self, point1, point2):
        point1.remove_lineto(point2)
        self.update()

    def highlight(self, point):
        point.hilight()
        self.update()

    def draw_animation(self):
        for k in range(0, len(self.points), 2):
            self.draw_line(self.origin, self.points[k], config.COLOR_LINE_SPECIAL)
            self.highlight(self.points[k])
            self.erase_line(self.origin, self.points[k])
            self.draw_line(self.origin, self.points[k + 1], config.COLOR_LINE_SPECIAL)
            self.highlight(self.points[k + 1])
            point = self.points[k]
            other_point = self.points[k + 1]
            self.draw_line(point, other_point, config.COLOR_PRIM)
            self.erase_line(self.origin, self.points[k + 1])
        self.erase_line(self.origin, self.points[len(self.points) - 1])
