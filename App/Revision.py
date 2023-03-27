import AppGlobals
from App.ChannelStrip import ChannelStrip
from App.StudioSetup import StudioSetup


class Revision:
    def __init__(self, studio: StudioSetup):
        self.name = 'Revision'
        self.studio = studio
        self.strips: list[ChannelStrip] = []

        self.strips.append(ChannelStrip(self.studio, AppGlobals.WidthType.Mono, 'Vox'))
        self.strips.append(ChannelStrip(self.studio, AppGlobals.WidthType.Stereo, 'Drums'))