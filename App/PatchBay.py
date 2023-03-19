from dataclasses import dataclass

import App.StudioSetup
from App.Point import Point
from AppGlobals import Socket
from App import StudioSetup
from App.GearItem import GearItem


# @dataclass
# class PatchPoint:
#     point: Point
#     device: GearItem
#

class PatchBay:
    def __init__(self, id: int, name: str, number_of_points: int):
        self.id: int = id
        self.name: str = name
        self.number_of_points: int = number_of_points
        self.points: list[Point] = [None] * self.number_of_points
        self.devices: list[GearItem] = [None] * self.number_of_points
        # print(self.points)

    def connect_gear(self, p: Point, device):
        point_index = p.point
        self.devices[point_index] = device
        self.points[point_index] = p

    def get_point_name(self, point):
        if self.devices[point] is not None:
            words = self.devices[point].name.split()
            shortname = str.join('\n', words)
            shortname += '\nIn' if self.points[point].type == Socket.Input else '\nOut'
            return shortname
        return f'-{point+1}-'

    def print_points(self):
        for i in range(self.number_of_points):
            name = ''
            if self.devices[i] is not None:
                name = self.devices[i].name
                print(name)
