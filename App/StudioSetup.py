import AppGlobals
from AppGlobals import Categories
from AppGlobals import WidthType
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
        self.patchbays.append(PatchBay.PatchBay(1, 'Outboard', 96))
        item = GearItem.GearItem('API 2500', Categories.Compressor, WidthType.Dual_Mono,
                                 [Point(0, 17, Socket.Input), Point(0, 18, Socket.Input),
                                  Point(0, 65, Socket.Output), Point(0, 66, Socket.Output)],
                                 1, 'imgs/api_2500_small.png', [])
        self.rack.append(item)

        lynx = GearItem.GearItem('Lynx', Categories.Interface, WidthType.Multi, [], 1, None, [])
        start_point = Point(0, 48, Socket.Input)
        end_point = Point(0, 63, Socket.Input)
        lynx.add_range(start_point, end_point)
        start_point = Point(0, 24, Socket.Output)
        end_point = Point(0, 39, Socket.Output)
        lynx.add_range(start_point, end_point)
        self.rack.append(lynx)
        self.populate_patches()
        # print(self.get_inputs())

    def new_gear(self) -> GearItem:
        item = GearItem.GearItem('New Gear',
                                 Categories.EQ,
                                 WidthType.Stereo, [], 1, None)
        self.rack.append(item)
        return item

    def populate_patches(self):
        for g in self.rack:
            p: Point
            for p in g.points:
                self.patchbays[p.patch_id].connect_gear(p, g)

    def get_interfaces(self):
        return [i for i in self.rack if i.category == Categories.Interface]

    def get_outboard(self):
        return [g for g in self.rack if g.category != Categories.Interface]

    def get_gear_by_name(self, name):
        for g in self.rack:
            if g.name == name:
                return g
        return None

    def get_io(self, width: WidthType, socket: Socket):
        io_list = []
        for i in self.get_interfaces():
            io_list += i.get_io(width, socket)
        return io_list

    # def get_inputs(self, width: WidthType):
    #     inputs = []
    #     for i in self.get_interfaces():
    #         inputs += i.get_inputs(width)
    #     return inputs
    #
    # def get_outputs(self, width: WidthType):
    #     outputs = []
    #     for i in self.get_interfaces():
    #         outputs += i.get_outputs(width)
    #     return outputs
    #

# self.inputs = []
# self.outputs = []
# self.interfaces: list[GearItem] = []
