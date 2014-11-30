# -*- coding: utf-8 -*-

from geocomp.common import control
from geocomp import config

class GraphicAnimation:
    def __init__(self, origin, points_list):
        self.origin = origin
        self.points = points_list

    def __update(self):
        control.thaw_update()
        control.update()
        control.freeze_update()
        control.sleep()

    def __draw_line(self, point1, point2, color):
        point1.lineto(point2, color)
        self.__update()

    def __erase_line(self, point1, point2):
        point1.remove_lineto(point2)
        self.__update()

    def __highlight(self, point, color = config.COLOR_HI_POINT):
        point.hilight(color)

    def __unhighlight(self, point):
        point.unhilight()

    def draw_animation(self):
        self.__highlight(self.origin, config.COLOR_POINT)
        self.__update()
        for k in range(0, len(self.points), 2):
            point = self.points[k]
            other_point = self.points[k + 1]
            self.__draw_line(self.origin, point, config.COLOR_LINE_SPECIAL)
            self.__highlight(point)
            self.__erase_line(self.origin, point)
            self.__draw_line(self.origin, other_point, config.COLOR_LINE_SPECIAL)
            self.__highlight(other_point)
            self.__draw_line(point, other_point, config.COLOR_PRIM)
            self.__erase_line(self.origin, other_point)
            self.__unhighlight(point)
            self.__unhighlight(other_point)
        self.__update()
        self.__unhighlight(self.origin)