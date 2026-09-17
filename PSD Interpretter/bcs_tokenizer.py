from enum import Enum
from psd_tools import constants

class TAG(Enum):
    text = "TEXT"

    # Text Formatting
    
    ## in runners
    bold = "\\b"
    italic = "\\i"
    underline = "\\u"
    strikethrough = "\\s"

    font_name = "\\fn"
    font_size = "\\fs"

    # Colors & Effects                      https://aegisub.org/docs/latest/ass_tags/#\c
    primary_color = "\\1c&H"
    outline_color = "\\3c&H"
    shadow_color  = "\\4c&H"
    primary_alpha = "\\1a&H"
    outline_alpha = "\\3a&H"
    shadow_alpha  = "\\4a&H"
    transparency  = "\\alpha&H"

    ## Effects
    ### Outlines                            https://aegisub.org/docs/latest/ass_tags/#\bord
    outline_width = "\\bord"
    outline_width_x = "\\xbord"
    outline_width_y = "\\ybord"

    ### Shadows                             https://aegisub.org/docs/latest/ass_tags/#\shad
    shadow_depth  = "\\shad"
    shadow_depth_x  = "\\xshad"
    shadow_depth_y  = "\\yshad"

    ### Blur                                https://aegisub.org/docs/latest/ass_tags/#\blur
    blur_edges = "\\be"
    blur = "\\blur"                         # This tag uses gaussian in normal but it's meaningless for my situation

    # Positioning
    pos = "\\pos"
    bbox = "\\bbox"

    ## Rotations                             https://aegisub.org/docs/latest/ass_tags/#\frx
    rotation_x = "\\frx"
    rotation_y = "\\fry"
    rotation_z = "\\frz"

    ## Font scale                            https://aegisub.org/docs/latest/ass_tags/#\fscx
    font_scale_x = "\\fscx"
    font_scale_y = "\\fscy"

    ## Text shearing                         https://aegisub.org/docs/latest/ass_tags/#\fax
    shear_x = "\\fax"
    shear_y = "\\fay"

    ## ALignment                             https://aegisub.org/docs/latest/ass_tags/#\an
    alignment = "\\an"

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

    @classmethod
    def from_just(self, justin: constants.Justification):
        match justin:
            case 0:
                return self(0)
            case 1:
                return self(2)
            case 2:
                return self(1)
            case 3:
                return self(0)
            case 4:
                return self(2)
            case 5:
                return self(1)
            case 6:
                return self(1)
            
class Line:
    Position: Token
    BoundingBox: Token
    Opacity: Token
    Rotation: Token
    Shear: Token
    FontScaleX: Token
    FontScaleY: Token
    text: str

    justification: Alignment
    effects: list[dict]

    def __str__(self):
        return f"{{\
{self.Position or ''}\
{self.BoundingBox or ''}\
{self.Opacity or ''}\
{self.Rotation or ''}\
{self.Shear or ''}\
{self.FontScaleX or ''}{self.FontScaleY or ''}\
{self.tag_justification() or ''}\
}}\
{self.text}"

    def tag_justification(self):
        if self.justification == Alignment.CENTER:
            return ""
        else:
            return Token("\\an", self.justification.value)

    def assign_transformations(self, tm):
        self.Rotation = Token("\\frz", tm["rotation_deg"])
        self.Shear = Token("\\fax", tm["shear_factor"])
        self.FontScaleX = Token("\\fscx", tm["scale_x"])
        self.FontScaleY = Token("\\fscy", tm["scale_y"])

class BCScript:
    styles: dict[dict]
    lines: list[Line]