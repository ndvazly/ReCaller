from enum import Enum


class Globals:
    def __init__(self):
        # """ UI Colors """
        self.DarkBG = '#071e26'
        self.ToolbarBG = '#0f3c4c'
        self.ButtonBG = '#92cbdf'
        self.PatchBG = '#AAB'
        self.TextColor = '#d4f1f8'

        # """ UI Fonts"
        self.HeaderFont = ('Arial', 18)
        self.NumberHeaderFont = ('Arial', 36)
        self.PatchFont = ('Arial', 10)

        # """ Paths & Data """
        self.ImgPath = 'imgs/'


class Socket(Enum):
    Input = 0
    Output = 1


class Categories(Enum):
    EQ = 1
    Compressor = 2
    Effect = 3
    Interface = 4


class WidthType(Enum):
    Mono = 1
    Stereo = 2
    Dual_Mono = 3
    Multi = 4


class Colors(Enum):
    Red     = [255, 0, 0]
    Green   = [0, 255, 0]
    Blue    = [0, 0, 255]

# @dataclass
# class Connection:
#     name: str
#     in_point: Point
#     out_point: Point
#
