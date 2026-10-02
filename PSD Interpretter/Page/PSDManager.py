from psd_tools import PSDImage, constants, color_convert, api
from psd_tools.api import layers
import psd_tools.psd.descriptor

from Page.bcs_tokenizer import *
from Page.interpretter import *
from meth import *

from warnings import warn

def text_layer(layer, Color_mode):
            line = Line(Token("\\pos", f"{layer.offset}"), Token("\\bbox", layer.size))

            if layer.fill_opacity != 255:
                line.Opacity = Token("\\1a&H", layer.fill_opacity)
            else:
                line.Opacity = None

            # Get layer's affine transformation and assign for .ass transformations
            tm = decompose_transform_matrix_for_ass_format(layer.transform)
            line.assign_transformations(tm)

            line.effects = effect_handler(layer.effects.items)

            font_name_buff = ""
            font_size_buff = 0
            fill_color_buff = ()

            ts = layer.typesetting
            for paragraph in ts:
                last_bold = False
                last_italics = False
                last_underline = False
                last_striketrough = False

                last_tracking = 0
                last_leading = 0

                line.justification = Alignment.from_just(paragraph.style.justification)
                for run in paragraph.runs:

                    tag_buffer: list[Token] = []

                    # Check font name to add tag_buffer
                    if run.style.font_name != font_name_buff:
                        tag_buffer.append(Token("\\fn", run.style.font_name))
                        font_name_buff = run.style.font_name

                    # Check font size to add tag_buffer
                    if run.style.font_size != font_size_buff:
                        tag_buffer.append(Token("\\fs", round(run.style.font_size * 1.3333)))
                        font_size_buff = run.style.font_size

                    # Check fill color to add tag_buffer
                    
                    # TODO: Add alpha channel and don't forget to layer opacity
                    # TODO: make sure to add compatibility for other color spaces
                    if run.style.fill_color != fill_color_buff:
                        match Color_mode:
                            case constants.ColorMode.BITMAP:
                                tag_buffer.append(Token("\\1c&B", f"{c8(run.style.fill_color[1])}&"))
                                fill_color_buff = run.style.fill_color
                            case constants.ColorMode.GRAYSCALE:
                                tag_buffer.append(Token("\\1c&G", f"{c8(run.style.fill_color[1])}&"))
                                fill_color_buff = run.style.fill_color
                            case constants.ColorMode.INDEXED:
                                tag_buffer.append(Token("\\1c&B", f"{c8(run.style.fill_color[1])}&"))
                                fill_color_buff = run.style.fill_color
                            case constants.ColorMode.RGB:
                                tag_buffer.append(Token("\\1c&H", f"{c8(run.style.fill_color[1])}{c8(run.style.fill_color[2])}{c8(run.style.fill_color[3])}&"))
                                fill_color_buff = run.style.fill_color
                            case constants.ColorMode.CMYK:
                                tag_buffer.append(Token("\\1c&C", f"{c8(run.style.fill_color[1])}{c8(run.style.fill_color[2])}{c8(run.style.fill_color[3])}{c8(run.style.fill_color[3])}&"))
                                fill_color_buff = run.style.fill_color
                            case constants.ColorMode.MULTICHANNEL:
                                tag_buffer.append(Token("\\1c&M", f"{c8(run.style.fill_color[1])}&"))
                                fill_color_buff = run.style.fill_color
                            case constants.ColorMode.DUOTONE:
                                tag_buffer.append(Token("\\1c&D", f"{c8(run.style.fill_color[1])}&"))
                                fill_color_buff = run.style.fill_color
                            case constants.ColorMode.LAB:
                                tag_buffer.append(Token("\\1c&L", f"{c8(run.style.fill_color[1])}{c8(run.style.fill_color[2])}{c8(run.style.fill_color[3])}&"))
                                fill_color_buff = run.style.fill_color

                    if run.style.faux_bold and ~last_bold:
                        tag_buffer.append(Token("\\b", "1"))
                        last_bold = True
                    if not(run.style.faux_bold) and last_bold:
                        tag_buffer.append(Token("\\b", "0"))
                        last_bold = False

                    if run.style.faux_italic and ~last_italics:
                        tag_buffer.append(Token("\\i", "1"))
                        last_italics = True
                    if not(run.style.faux_italic) and last_italics:
                        tag_buffer.append(Token("\\i", "0"))
                        last_italics = False

                    if run.style.underline and ~last_underline:
                        tag_buffer.append(Token("\\u", "1"))
                        last_underline = True
                    if not(run.style.underline) and last_underline:
                        tag_buffer.append(Token("\\u", "0"))
                        last_underline = False

                    if run.style.strikethrough and ~last_striketrough:
                        tag_buffer.append(Token("\\s", "1"))
                        last_striketrough = True
                    if not(run.style.strikethrough) and last_striketrough:
                        tag_buffer.append(Token("\\s", "0"))
                        last_striketrough = False

                    if run.style.tracking != last_tracking:
                        last_tracking = run.style.tracking
                        tag_buffer.append(Token("\\fsp", last_tracking))
                    if run.style.leading != last_leading:
                        last_leading = run.style.leading
                        tag_buffer.append(Token("\\fle", last_leading))

                    single_tag = ""

                    if tag_buffer:
                        single_tag += "{"
                        for tag in tag_buffer:
                            single_tag += f"{tag.tag}:{tag.value}"
                        single_tag += "}"

                    single_tag += run.text

                    if tag_buffer:
                        single_tag += "{"
                        for tag in tag_buffer:

                            single_tag += f"{tag.tag}"
                        single_tag += "}"

                    line.text = single_tag
                    # print("result:", line)
                    return (line, font_name_buff)

class PSD_Page:
    psd: PSDImage
    bscript: Page
    # list of fonts in the psd file for font gathering process
    fontset = []
    Color_mode: constants.ColorMode

    def __init__(self, psd_file, ind):
        self.psd = PSDImage.open(psd_file)
        self.bscript = Page()
        print(f"psd içindeki katmanlar: {self.psd.__len__()}")
        self.Color_mode = self.psd.color_mode
        self.bscript.number = ind

    def loopy_loopy(self, layer: layers.Layer):
        match layer.kind:
            case "group":
                for lay in layer:
                    self.loopy_loopy(lay)
            case "pixel":
                # TODO: Add rasterizing of neighbor pixel layers
                # TODO: UI: Add setting some layers to be in the base folder
                self.bscript.lines.append(PixelLayer(layer.composite(), Token("\\pos", layer.offset), Token("\\bbox", layer.bbox), Token("\\1a&H", layer.fill_opacity), layer.name))
            case "type":
                text_lay = text_layer(layer, self.Color_mode)
                self.bscript.lines.append(text_lay[0])
                self.fontset += text_lay[1]
            case _:
                warn("Some layers ignored please rasterize all layers except pixel, type(text) or group")

def read_psd_and_tokenize(psd_file, index):
    psd_c = PSD_Page(psd_file, index)
    print(f"reading {index} psd:")

    for layer in psd_c.psd:
        psd_c.loopy_loopy(layer)
    print(f"number of layers: {psd_c.bscript.lines.__len__()}")

    return psd_c.bscript