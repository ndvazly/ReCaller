from AppGlobals import Categories
from AppGlobals import Types
from AppGlobals import Connection
from AppGlobals import Point
from App import PatchBay
from App import GearItem


class StudioSetup:
    def __init__(self, name):
        self.name = name
        self.patchbays: PatchBay = []
        self.inputs = []
        self.outputs = []
        self.rack: list(GearItem) = []

        self.patchbays.append(PatchBay.PatchBay(0, 'I/O Patch', 96))
        item = GearItem.GearItem('API 2500', Categories.Compressor, Types.Dual_Mono,
                                 Point(0, 1), Point(0, 45), 1, 'imgs/api_2500_small.png', False)
        # item = GearItem.GearItem('API 2500', Categories.Compressor, Types.Dual_Mono,
        #                          Connection("API 2500", 1, 45), 1, 'imgs/api_2500_small.png', False)
        self.rack.append(item)

        self.add_input("Lynx In 1", Point(0, 16))
        self.patchbays[0].populate_patch(self)

    def add_input(self, name: str, point: Point):
        # self.inputs.append({name: point})
        self.inputs.append({'name': name, 'point': point})
