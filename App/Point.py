from dataclasses import dataclass
from AppGlobals import Socket


@dataclass
class Point:
    patch_id: int
    point: int
    type: Socket
    name: str = ''
