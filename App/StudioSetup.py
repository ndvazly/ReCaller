import AppGlobals
from AppGlobals import Categories
from AppGlobals import Types
from AppGlobals import Socket
from App.Point import Point
from App import PatchBay
from App import GearItem


class StudioSetup:
    def __init__(self, name):
        self.name = name
        self.patchbays: list[PatchBay] = []
        self.rack: list[GearItem] = []

        self.patchbays.append(PatchBay.PatchBay(0, 'I/O Patch', 96))
        item = GearItem.GearItem('API 2500', Categories.Compressor, Types.Dual_Mono,
                                 [Point(0, 17, Socket.Input), Point(0, 45, Socket.Output)], 1, 'imgs/api_2500_small.png', False)
        self.rack.append(item)

        lynx = GearItem.GearItem('Lynx', Categories.Interface, Types.Multi, [], 1, None, False)
        start_point = Point(0, 48, Socket.Input)
        end_point = Point(0, 63, Socket.Input)
        lynx.add_range(start_point, end_point)
        # self.interfaces.append(lynx)
        self.rack.append(lynx)
        self.populate_patches()

    def populate_patches(self):
        for g in self.rack:
            p: Point
            for p in g.points:
                self.patchbays[p.patch_id].connect_gear(p, g)

# self.inputs = []
# self.outputs = []
# self.interfaces: list[GearItem] = []
