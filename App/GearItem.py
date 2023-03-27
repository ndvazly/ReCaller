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
    width_type: WidthType
    points: list[Point]
    color: Colors
    img_file: str

    def add_point(self, point: Point):
        self.points.append(point)

    def add_range(self, start_point: Point, end_point: Point):
        for i in range(start_point.point, end_point.point+1):
            self.add_point(Point(start_point.patch_id, i, start_point.type))

    def get_io(self, width: WidthType, socket: Socket):
        io_list = [p for p in self.points if p.type == socket]
        if width == WidthType.Mono:
            return io_list
        # Get Stereo In/Out
        stereo_list = []
        i = 0
        while i < len(io_list):
            if io_list[i].name == io_list[i+1].name:
                stereo_list.append((io_list[i], io_list[i+1]))
            i += 2
        return stereo_list
