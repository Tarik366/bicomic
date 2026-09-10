from psd_tools import PSDImage, constants, color_convert, api
from psd_tools.api.effects import _Effect
import psd_tools.psd.descriptor
import json
from json import JSONEncoder

psd = PSDImage.open('unicorn-controller.psd')
psd.composite().save('example.png')

class Line:
    BoundingBox: tuple
    text: str

    style: str
    fontSize: int
    fillColor: tuple
    justification: constants.Justification
    effects: list[dict]



class BCScript:
    styles: dict[dict]
    lines: list[Line]

def Descriptor_to_dickt(val):
    if isinstance(val, psd_tools.psd.descriptor.Bool):
        return bool(val.value)

    elif isinstance(val, psd_tools.psd.descriptor.Enumerated):
        return val.get_name()

    elif isinstance(val, psd_tools.psd.descriptor.UnitFloat):
        return {"value": val.value, "unit": val.unit.value.decode()}

    elif isinstance(val, psd_tools.psd.descriptor.Double):
        return val.value

    elif isinstance(val, psd_tools.psd.descriptor.Descriptor):
        clr = {}
        for chan, col in val.items():
            clr[chan.decode()] = Descriptor_to_dickt(col)
        return clr

    elif isinstance(val, psd_tools.psd.descriptor.List):
        li = [] 
        for it in val._items:
            li.append(Descriptor_to_dickt(it))
        return li

    else:
        return val

with open("export.bcs","w") as BCScriptFile:

    # list of fonts in the psd file for font gathering process
    bscript = BCScript()
    fontset = []

    for layer in psd:
        if layer.kind == "type":
            line = Line()

            line.BoundingBox = layer.size + layer.offset
            line.text = layer.text

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

            text_buff = ""

            ts = layer.typesetting
            for paragraph in ts:

                line = constants.Justification(paragraph.style.justification)
                for run in paragraph.runs:

                    if run.style.font_name != font_name_buff[-1:]:
                        text_buff += f"{{}}{run.style.font_name}"
                        font_name_buff.append(run.style.font_name)
                    if run.style.font_size != font_size_buff[-1:]:
                        print(f"yeni font boyutu: {run.style.font_size}")
                        font_size_buff.append(run.style.font_size)
                    if run.style.fill_color != fill_color_buff[-1:]:
                        print(f"yeni font rengi: {run.style.fill_color}")

                        fill_color_buff.append(run.style.fill_color)

                    print(font_name_buff)

                    print(f"{run.text};{run.style.font_name};{round(run.style.font_size * 1.3333)};{run.style.fill_color};\n")

                    # TODO: Convert text layers into bcscript file