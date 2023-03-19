from dataclasses import dataclass
from AppGlobals import *
from App.Point import Point


@dataclass
class GearItem:
    """Class for keeping track of an outboard gear item.\n
        name: str\n
        category: Categories\n
        type: Types\n
        in_point: Point
        out_point: Point
        color: Colors\n
        img_file: str\n
        in_use: bool\n
    """
    name: str
    category: Categories
    type: Types
    points: list[Point]
    color: Colors
    img_file: str
    in_use: bool

    def add_point(self, point: Point):
        self.points.append(point)

    def add_range(self, start_point: Point, end_point: Point):
        for i in range(start_point.point, end_point.point+1):
            self.add_point(Point(start_point.patch_id, i, start_point.type))
