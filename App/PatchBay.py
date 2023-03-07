from dataclasses import dataclass
from AppGlobals import Point
from App import StudioSetup


# @dataclass
class PatchBay:
    def __init__(self, id: int, name: str, number_of_points: int):
        self.id: int = id
        self.name: str = name
        self.number_of_points: int = number_of_points
        self.points: list = []

    def populate_patch(self, studio: StudioSetup):
        for i in studio.inputs:
            if i['point'].patch_id == self.id:
                self.points.append({'point': i['point']})
