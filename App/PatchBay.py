from App.Point import Point


class PatchBay:
    def __init__(self, id: int, name: str, number_of_points: int):
        self.id: int = id
        self.name: str = name
        self.number_of_points: int = number_of_points
        self.points: list[Point] = [None] * self.number_of_points
        # self.devices: list[GearItem] = [None] * self.number_of_points
        # print(self.points)

    def clear(self):
        self.points: list[Point] = [None] * self.number_of_points

    def connect_gear(self, p: Point, device):
        point_index = p.point
        p.gear = device
        self.points[point_index] = p

    def get_point_name(self, point):
        if self.points[point] is not None:
            return self.points[point].get_short_name()
        return f'-{point+1}-'

    def print_points(self):
        for i in range(self.number_of_points):
            name = ''
            if self.devices[i] is not None:
                name = self.devices[i].name
                print(name)