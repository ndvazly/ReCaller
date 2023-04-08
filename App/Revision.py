from App.ChannelStrip import ChannelStrip
from App.StudioSetup import StudioSetup


class Revision:
    def __init__(self, name, studio: StudioSetup):
        self.name = name
        self.studio = studio
        self.strips: list[ChannelStrip] = []
        self.notes: str = ''

    def set_studio(self, studio: StudioSetup):
        self.studio = studio
        for s in self.strips:
            s.studio = self.studio

    def new_strip(self, strip_name, strip_width):
        self.strips.append(ChannelStrip(self.studio, strip_width, strip_name))

    def get_str(self) -> str:
        txt = self.name + '\n'
        txt += '-' * len(self.name) + '\n'
        for s in self.strips:
            txt += s.strip_str()
        if self.notes != '':
            txt += '\n' + self.notes + '\n'
        print(txt)
        return txt
