from enum import Enum
from psd_tools import constants

# TODO: Turn this into a extended python C library 
# [1]: https://docs.python.org/3/extending/extending.html

class TAG(Enum):
    text = "TEXT"

    # Text Formatting
    
    ## in runners
    bold_start = "\\b1"
    bold_end = "\\b0"
    italic_start = "\\i1"
    italic_end = "\\i0"
    underline_start = "\\u1"
    underline_end = "\\u0"
    Strikethrough_start = "\\s1"
    Strikethrough_end = "\\s0"
    font_name = "\\fn"
    font_size = "\\fs"

    ## text layer

    # Colors & Effects
    primary_color = "\\c&H"
    outline_color = "\\3c&H"
    shadow_color  = "\\4c&H"
    transparency  = "\\alpha&H"
    outline_width = "\\bord"
    shadow_depth  = "\\shad"
    blur = "\\blur"

    # Positioning
    pos = "\\pos"
    ### Bounding box
    bbox = "\\bbox"

class Token:
    tag: TAG
    value: str

    def __init__(self, tag, value = ""):
        self.tag = tag
        self.value = value

    def __str__(self):
        return f"{self.tag}:{self.value}"

    def __repr__(self):
        return str(self)

class Alignment(Enum):

    LEFT = 0
    CENTER = 1
    RIGHT = 2

    def __init__(self, justin: constants.Justification):
        match justin:
            case 0:
                return 0
            case 1:
                return 2
            case 2:
                return 1
            case 3:
                return 0
            case 4:
                return 2
            case 5:
                return 1
            case 6:
                return 1
            

class Line:
    Position: Token
    BoundingBox: Token
    text: str

    justification: Alignment
    effects: list[dict]

    def __str__(self):
        return f"{{{self.Position}{self.BoundingBox}}}{self.text}"