from dataclasses import dataclass
from AppGlobals import *


@dataclass
class GearItem:
    """Class for keeping track of an outboard gear item.\n
        name: str\n
        category: Categories\n
        type: Types\n
        in_point: Point
        out_point: Point
        color: Colors\n
        img_file: str\n
        in_use: bool\n
    """
    name: str
    category: Categories
    type: Types
    # connection: Connection
    in_point: Point
    out_point: Point
    color: Colors
    img_file: str
    in_use: bool
