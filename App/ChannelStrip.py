import AppGlobals
from AppGlobals import WidthType, Socket
from App.Point import Point
from App.StudioSetup import StudioSetup
from App.GearItem import GearItem


class ChannelStrip:
    def __init__(self, studio: StudioSetup, width: WidthType, name: str = ''):
        self.name = name
        self.width: WidthType = width
        self.studio: StudioSetup = studio
        self.input: list[Point] = []
        self.output: list[Point] = []
        self.inserts: list[GearItem] = [None] * 4
        self.settings: list = [None] * 4
        self.color: AppGlobals.Colors = AppGlobals.Colors.Green
        self.select_io(Socket.Input, 0)
        self.select_io(Socket.Output, 0)

    def select_io(self, socket, index):
        if socket == Socket.Input:
            self.input = self.get_io_list(socket)[index]
        else:
            self.output = self.get_io_list(socket)[index]

    def get_gear_name(self, name: str):
        if name.endswith('>'):
            return name[:name.index('<')-1]
        return name

    def get_dual_mono_index(self, name: str):
        if name.endswith('>'):
            left_or_right = name[name.index('<')+1]
            if left_or_right == 'L':
                return 0
            else:
                return 1
        return 0

    def select_insert(self, index, name):
        self.inserts[index] = name
        self.settings[index] = []
        if name == '':
            return
        gear: GearItem = self.studio.get_gear_by_name(self.get_gear_name(name))
        for s in gear.settings:
            self.settings[index].append({'name': s['name'],'value': ''})
        self.get_chain()

    def get_chain(self):
        chain: list[Point] = [self.output]
        for i in self.inserts:
            if i is None or i == '':
                continue
            gear: GearItem = self.studio.get_gear_by_name(self.get_gear_name(i))
            left_right = self.get_dual_mono_index(i)
            gear_input = gear.get_io(self.width, Socket.Input)
            chain.append(gear_input[left_right])
            gear_output = gear.get_io(self.width, Socket.Output)
            chain.append(gear_output[left_right])
        chain.append(self.input)
        self.print_chain(chain)

    def print_chain(self, chain):
        print(f'---{self.name} Chain ---')
        p: Point = None
        for p in chain:
            if type(p) is tuple:
                for i in p:
                    i.print()
            else:
                p.print()

    def get_io_list(self, socket):
        return [i for i in self.studio.get_io(self.width, socket)]

    def get_available_io_names(self, socket: Socket):
        # io_list = [i for i in self.studio.get_io(self.width, socket)]
        io_list = self.get_io_list(socket)
        io_names = []
        if self.width == WidthType.Mono:
            for i in range(len(io_list)):
                io_names.append(io_list[i].get_name() + f' {i+1}')
        else:
            index = 0
            for i in range(len(io_list)):
                io_names.append(io_list[i][0].get_name() + f' {index+1}-{index+2}')
                index += 2
        return io_names

    # def check_width(self, width):
    #     if self.width == WidthType.Mono:
    #         return True
    #     else:
    #         return width != WidthType.Mono

    def get_outboard_names(self):
        outboard = self.studio.get_outboard()
        names_list = []
        if self.width == WidthType.Mono:
            g: GearItem = None
            for g in outboard:
                if g.width_type == WidthType.Multi:
                    for index in range(len(g.get_io(WidthType.Mono, Socket.Input))):
                        names_list.append(g.name + f' <{index+1}>')
                elif g.width_type == WidthType.Dual_Mono:
                    names_list.append(g.name + ' <L>')
                    names_list.append(g.name + ' <R>')
                elif g.width_type == WidthType.Stereo or g.width_type == WidthType.Mono:
                    names_list.append(g.name)
            return [''] + names_list
                    # return [''] + [g.name for g in outboard]
        names_list = []
        for g in outboard:
            if g.width_type.value > 1:
                names_list.append(g.name)
        return [''] + names_list

