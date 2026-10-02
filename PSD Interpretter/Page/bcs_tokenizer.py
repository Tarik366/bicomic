from enum import Enum
from psd_tools import constants
from PIL import Image

import zipfile

class TAG(Enum):
    text = "TEXT"

    # Text Formatting
    
    ## in runners
    bold = "\\b"                     # V
    italic = "\\i"                   # V
    underline = "\\u"                # V
    strikethrough = "\\s"            # V

    font_name = "\\fn"               # V
    font_size = "\\fs"               # V
    font_tracking = "\\fsp"          # V
    font_leading = "\\fle"           # V    This is a custom tag that don't exist in Aegisub and will be ignored by any subtitle app

    # Colors & Effects                      https://aegisub.org/docs/latest/ass_tags/#\c
    primary_color = "\\1c&H"         # V
    outline_color = "\\3c&H"
    shadow_color  = "\\4c&H"
    primary_alpha = "\\1a&H"
    outline_alpha = "\\3a&H"
    shadow_alpha  = "\\4a&H"
    transparency  = "\\alpha&H"      # V

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
    pos = "\\pos"                    # V
    bbox = "\\bbox"                  # V

    ## Rotations                             https://aegisub.org/docs/latest/ass_tags/#\frx
    rotation_x = "\\frx"             # V
    rotation_y = "\\fry"             # V
    rotation_z = "\\frz"

    ## Font scale                            https://aegisub.org/docs/latest/ass_tags/#\fscx
    font_scale_x = "\\fscx"          # V
    font_scale_y = "\\fscy"          # V

    ## Text shearing                         https://aegisub.org/docs/latest/ass_tags/#\fax
    shear_x = "\\fax"                # V
    shear_y = "\\fay"                # V

    ## ALignment                             https://aegisub.org/docs/latest/ass_tags/#\an
    alignment = "\\an"               # V

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
    Opacity: Token | None
    Rotation: Token
    Shear: Token
    FontScaleX: Token
    FontScaleY: Token
    text: str = ""

    justification: Alignment
    effects: list[dict]

    def __init__(self, pos, bbox, opacity = None, Rotation = Token("\\frz", "0.0"), Shear = Token("\\frz", "0.0"), FontScaleX = Token("\\frz", "1.0"), FontScaleY = Token("\\frz", "1.0"), just = Alignment.CENTER):
        self.Position, self.BoundingBox, self.Opacity = pos, bbox, opacity
        self.Rotation, self.Shear, self.FontScaleX, self.FontScaleY = Rotation, Shear, FontScaleX, FontScaleY
        self.justification = just

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
{self.text}\n"

    def __repr__(self):
        return self.__str__()

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

class PixelLayer(Line):
    name: str
    data: Image.Image

    def __init__(self, image, pos, bbox, alpha, name):
        super().__init__(pos, bbox, alpha)
        self.data = image
        self.name = name

    def __repr__(self):
            return f"p{{\
{self.Position or ''}\
{self.BoundingBox or ''}\
{self.Opacity or ''}\
{self.Rotation or ''}\
{self.Shear or ''}\
{self.FontScaleX or ''}{self.FontScaleY or ''}\
{self.tag_justification() or ''}\
}}\
{self.name}.avif\n"

class Page:
    lines: list[Line]
    number = 0
    language: str

    def __init__(self, lang = "eng"):
        self.lines = []
        self.language = lang

    def __str__(self):
        bufger = ""
        for li in self.lines:
            bufger += li.__repr__()
        return bufger

    # TODO: Make this thing to be in the recursive matroska loop
    def export(self, filename):
        with zipfile.ZipFile(filename, "w", 14) as zf:
            zf.writestr("typeset.bcs", self.__str__())
            print(f"İşlenecek katmanlar: {self.lines.__len__()}")
            for lay in self.lines:
                if isinstance(lay, PixelLayer):
                    print(lay.name)
                    zf.writestr(f"{self.number}/{lay.name}.avif", lay.data._repr_image("avif", alpha_premultiplied=True))
