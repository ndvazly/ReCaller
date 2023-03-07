from enum import Enum
from dataclasses import dataclass


class Globals:
    def __init__(self):
        # """ UI Colors """
        self.DarkBG = '#071e26'
        self.ToolbarBG = '#0f3c4c'
        self.ButtonBG = '#92cbdf'
        self.TextColor = '#d4f1f8'

        # """ UI Fonts"
        self.HeaderFont = ('Arial', 16)

        # """ Paths & Data """
        self.ImgPath = 'imgs/'


class Categories(Enum):
    EQ = 1
    Compressor = 2
    Effect = 3


class Types(Enum):
    Mono = 1
    Stereo = 2
    Dual_Mono = 3


class Colors(Enum):
    Red     = [255, 0, 0]
    Green   = [0, 255, 0]
    Blue    = [0, 0, 255]


@dataclass
class Point:
    patch_id: int
    point: int


@dataclass
class Connection:
    name: str
    in_point: Point
    out_point: Point
