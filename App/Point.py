from dataclasses import dataclass
from AppGlobals import Socket


@dataclass
class Point:
    patch_id: int
    point: int
    type: Socket
    name: str = ''
    gear = None
    in_use: bool = False

    def get_name(self):
        name = self.gear.name + ' ' + self.name + ' '
        name_lower = self.name.lower()
        if 'rtrn' not in name_lower and 'send' not in name_lower and 'return' not in name_lower:
            name += 'In' if self.type == Socket.Input else 'Out'
        return name

    def get_short_name(self):
        words = self.gear.name.split()
        shortname = str.join('\n', words)
        if self.name != '':
            shortname += '\n' + self.name
        shortname += '\nIn' if self.type == Socket.Input else '\nOut'
        return shortname

    def print(self):
        print(f'{self.gear.name}: {self.patch_id}|{self.point} -> {self.type.name}')