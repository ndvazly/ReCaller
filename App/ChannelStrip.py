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
        self.notes: str = ''
        self.input: list[Point] = []
        self.output: list[Point] = []
        self.input_str: str = ''
        self.output_str: str = ''
        self.input_index: int = 0
        self.output_index: int = 0
        self.inserts: list[GearItem] = [None] * 4
        self.settings: list = [None] * 4
        self.color: AppGlobals.Colors = AppGlobals.Colors.Green
        self.select_io(Socket.Input, 0)
        self.select_io(Socket.Output, 0)

    def select_io(self, socket, index):
        if len(self.get_io_list(socket)) == 0:
            return
        if socket == Socket.Input:
            self.input = self.get_io_list(socket)[index]
            self.input_index = index
            self.input_str = self.get_available_io_names(socket)[index]
        else:
            self.output = self.get_io_list(socket)[index]
            self.output_index = index
            self.output_str = self.get_available_io_names(socket)[index]

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
            self.settings[index].append({'name': s['name'], 'value': '', 'type': s['value']})
        self.get_chain()

    def strip_str(self):
        txt = ''
        if self.name != '':
            txt = self.name + ': '
        txt += '(' + self.output_str + ' -> ' + self.input_str + ')\n'
        txt += self.insert_str(0)
        txt += self.insert_str(1)
        txt += self.insert_str(2)
        txt += self.insert_str(3)
        return txt

    def insert_str(self, index) -> str:
        txt = self.inserts[index]
        if txt is None:
            return ''
        txt = '\t' + txt + '\n\t'
        for s in self.settings[index]:
            txt += s['name'] + ': '
            if s['type'] == 'On/Off':
                txt += 'On' if s['value'] == 1 else 'Off'
            else:
                txt += str(s['value'])
            txt += ', '
        txt = txt[:len(txt)-2]
        return txt + '\n\n'

    def get_chain(self):
        chain: list[Point] = [self.output]
        for i in self.inserts:
            if i is None or i == '':
                continue
            gear: GearItem = self.studio.get_gear_by_name(self.get_gear_name(i))
            left_right = self.get_dual_mono_index(i)
            gear_input = gear.get_io(self.width, Socket.Input)
            if len(gear_input) == 0:
                continue
            chain.append(gear_input[left_right])
            gear_output = gear.get_io(self.width, Socket.Output)
            chain.append(gear_output[left_right])
        chain.append(self.input)
        # self.print_chain(chain)

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
            input_index = 0
            prev_name = ''
            for i in range(len(io_list)):
                name = io_list[i].get_name()
                if prev_name != name:
                    input_index = 0
                io_names.append(name + f' {input_index+1}')
                prev_name = name
                input_index += 1
        else:
            index = 0
            prev_name = ''
            for i in range(len(io_list)):
                name = io_list[i][0].get_name()
                if prev_name != name:
                    index = 0
                io_names.append(name + f' {index+1}-{index+2}')
                prev_name = name
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

