from psd_tools import PSDImage, constants, color_convert, api
from psd_tools.api.effects import _Effect
import psd_tools.psd.descriptor
import json
from json import JSONEncoder

from bcs_tokenizer import Token, Line, Alignment

psd = PSDImage.open('unicorn-controller.psd')
psd.composite().save('example.png')

class BCScript:
    styles: dict[dict]
    lines: list[Line]

def Descriptor_to_dickt(val):
    match type(val):
        case psd_tools.psd.descriptor.Bool:
            return bool(val.value)

        case psd_tools.psd.descriptor.Enumerated:
            return val.get_name()

        case psd_tools.psd.descriptor.UnitFloat:
            return {"value": val.value, "unit": val.unit.value.decode()}

        case psd_tools.psd.descriptor.Double:
            return val.value

        case psd_tools.psd.descriptor.Descriptor:
            clr = {}
            for chan, col in val.items():
                clr[chan.decode()] = Descriptor_to_dickt(col)
            return clr

        case psd_tools.psd.descriptor.List:
            li = [] 
            for it in val._items:
                li.append(Descriptor_to_dickt(it))
            return li

        case _:
            return val

def lerp(v0, v1, t):
    return (1 - t) * v0 + t * v1

def c8(run):
    return f"{int(lerp(0, 255, run)):02x}"

with open("export.bcs","w") as BCScriptFile:

    # list of fonts in the psd file for font gathering process
    bscript = BCScript()
    fontset = []

    for layer in psd:

        if layer.kind == "type":
            line = Line()

            line.Position = Token("\\pos", f"{layer.offset[0]}")
            line.BoundingBox = Token("\\bbox", layer.size)

            effect_list = []
            for effect in layer.effects.items:
                copy_of_descriptor = {}
                for key, val in effect.__dict__["descriptor"].items():
                    copy_of_descriptor[key.decode()] = Descriptor_to_dickt(val)
                effect_list.append(copy_of_descriptor)
            line.effects = effect_list

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
                    

                    print("single_tag:", single_tag)

                    line.text = single_tag
                    print("result:", line)
                    # TODO: Convert text layers into bcscript file

            BCScriptFile.write("\n")