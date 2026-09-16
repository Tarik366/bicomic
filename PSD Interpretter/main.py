from psd_tools import PSDImage, constants, color_convert, api
from psd_tools.api.effects import _Effect
import psd_tools.psd.descriptor

from bcs_tokenizer import *
from interpretter import *
from meth import *

psd = PSDImage.open('unicorn-controller.psd')
psd.composite().save('example.png')

with open("export.bcs","w") as BCScriptFile:

    bscript = BCScript()
    # list of fonts in the psd file for font gathering process
    fontset = []

    for layer in psd:

        if layer.kind == "type":
            line = Line()

            line.Position = Token("\\pos", f"{layer.offset}")
            line.BoundingBox = Token("\\bbox", layer.size)

            line.Opacity = Token("\\1a&H", layer.fill_opacity)

            tm = decompose_transform_matrix_for_ass_format(layer.transform)

            line.Rotation = Token("\\frz", tm["rotation_deg"])
            line.Shear = Token("\\fax", tm["shear_factor"])
            line.FontScaleX = Token("\\fscx", tm["scale_x"])
            line.FontScaleY = Token("\\fscy", tm["scale_y"])

            effect_list = effect_handler(layer.effects.items)

            text = layer.engine_dict['Editor']['Text'].value

            font_name_buff = []
            font_size_buff = []
            fill_color_buff = []

            text_buff = []

            ts = layer.typesetting
            for paragraph in ts:

                line.justification = Alignment.from_just(paragraph.style.justification)
                for run in paragraph.runs:

                    tag_buffer: list[Token] = []

                    # Check font name to add tag_buffer
                    try:
                        if run.style.font_name != font_name_buff[-1]:
                            tag_buffer.append(Token("\\fn", run.style.font_name))
                            font_name_buff.append(run.style.font_name)
                    except IndexError:
                        tag_buffer.append(Token("\\fn", run.style.font_name))
                        font_name_buff.append(run.style.font_name)

                    # Check font size to add tag_buffer
                    try:
                        if run.style.font_size != font_size_buff[-1]:
                            tag_buffer.append(Token("\\fs", round(run.style.font_size * 1.3333)))
                            font_size_buff.append(run.style.font_size)
                    except IndexError:
                        tag_buffer.append(Token("\\fs", round(run.style.font_size * 1.3333)))
                        font_size_buff.append(run.style.font_size)

                    # Check fill color to add tag_buffer
                    try:
                        # TODO: Add alpha channel and don't forget to layer opacity
                        if run.style.fill_color != fill_color_buff[-1]:
                            tag_buffer.append(Token("\\1c&H", f"{c8(run.style.fill_color[1])}{c8(run.style.fill_color[2])}{c8(run.style.fill_color[3])}&"))
                            fill_color_buff.append(run.style.fill_color)
                    except IndexError:
                        tag_buffer.append(Token("\\1c&H", f"{c8(run.style.fill_color[1])}{c8(run.style.fill_color[2])}{c8(run.style.fill_color[3])}&"))
                        fill_color_buff.append(run.style.fill_color)

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
                    print("result:", line)
                    # TODO: Convert text layers into bcscript file

            BCScriptFile.write("\n")