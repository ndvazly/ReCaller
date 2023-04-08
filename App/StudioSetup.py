from AppGlobals import Categories
from AppGlobals import WidthType
from AppGlobals import Socket
from App.Point import Point
from App import PatchBay
from App import GearItem
import pickle


class StudioSetup:
    def __init__(self, name):
        self.name = name
        self.patchbays: list[PatchBay] = []
        self.rack: list[GearItem] = []

        self.populate_patches()
        # self.patchbays[0].print_points()

    def new_gear(self) -> GearItem:
        item = GearItem.GearItem('New Gear',
                                 Categories.EQ,
                                 WidthType.Stereo, [], 1, None, [])
        self.rack.append(item)
        return item

    def populate_patches(self):
        for i in range(len(self.patchbays)):
            self.patchbays[i].clear()
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

    def save(self):
        with open('studio.pkl', 'wb') as f:
            pickle.dump(self, f)
            print('Studio Setup Saved')