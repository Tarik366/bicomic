from psd_tools import PSDImage, constants, color_convert, api
from psd_tools.api.effects import _Effect
import psd_tools.psd.descriptor

from bcs_tokenizer import *
from interpretter import *

psd = PSDImage.open('unicorn-controller.psd')
psd.composite().save('example.png')


def lerp(v0, v1, t):
    return (1 - t) * v0 + t * v1

def c8(run):
    return f"{int(lerp(0, 255, run)):02x}"

with open("export.bcs","w") as BCScriptFile:

    bscript = BCScript()
    # list of fonts in the psd file for font gathering process
    fontset = []

    for layer in psd:

        if layer.kind == "type":
            line = Line()

            line.Position = Token("\\pos", f"{layer.offset[0]}")
            line.BoundingBox = Token("\\bbox", layer.size)

            effect_list = effect_handler(layer.effects.items)

            text = layer.engine_dict['Editor']['Text'].value
            print(layer.text)

            font_name_buff = []
            font_size_buff = []
            fill_color_buff = []

            text_buff = []

            ts = layer.typesetting
            for paragraph in ts:

                line.justification = Alignment(paragraph.style.justification)
                for run in paragraph.runs:

                    tag_buffer: list[Token] = []

                    try:
                        if run.style.font_name != font_name_buff[-1]:
                            tag_buffer.append(Token("\\fn", run.style.font_name))
                            font_name_buff.append(run.style.font_name)
                    except IndexError:
                        tag_buffer.append(Token("\\fn", run.style.font_name))
                        font_name_buff.append(run.style.font_name)

                    try:
                        if run.style.font_size != font_size_buff[-1]:
                            tag_buffer.append(Token("\\fs", round(run.style.font_size * 1.3333)))
                            font_size_buff.append(run.style.font_size)
                    except IndexError:
                        tag_buffer.append(Token("\\fs", round(run.style.font_size * 1.3333)))
                        font_size_buff.append(run.style.font_size)

                    try:
                        # TODO: Add alpha channel and don't forget to layer opacity
                        if run.style.fill_color != fill_color_buff[-1]:
                            tag_buffer.append(Token("\\c&H", f"{c8(run.style.fill_color[1])}{c8(run.style.fill_color[2])}{c8(run.style.fill_color[3])}&"))
                            fill_color_buff.append(run.style.fill_color)
                    except IndexError:
                        tag_buffer.append(Token("\\c&H", f"{c8(run.style.fill_color[1])}{c8(run.style.fill_color[2])}{c8(run.style.fill_color[3])}&"))
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