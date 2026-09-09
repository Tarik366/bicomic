from psd_tools import PSDImage, constants, color_convert, api
from psd_tools.api.effects import _Effect
import psd_tools.psd.descriptor
import json
from json import JSONEncoder

psd = PSDImage.open('unicorn-controller.psd')
psd.composite().save('example.png')

class Line:
    BoundingBox: tuple
    style: str
    fontSize: int
    fillColor: tuple
    strokeColor: tuple
    strokeSize: int
    justification: constants.Justification


class BCScript:
    styles: dict[dict]
    lines: Line

"""class BEffect(_Effect):
    def to_json(self):
        """

class EncodeStudent(JSONEncoder):
    def default(self, o):
        return o.__dict__

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

with open("export.bcs","w") as BCScript:

    # list of fonts in the psd file for font gathering process
    fontset = []

    for layer in psd:
        if layer.kind == "type":
            BCScript.write(f"{layer.size}, {layer.offset};\n")
            BCScript.write(f"{layer.text};\n")

            print(layer.effects.items)
            effect_list = []
            for effect in layer.effects.items:
                copy_of_descriptor = {}
                for key, val in effect.__dict__["descriptor"].items():
                    copy_of_descriptor[key.decode()] = Descriptor_to_dickt(val)
                effect_list.append(copy_of_descriptor)

            text = layer.engine_dict['Editor']['Text'].value

            ts = layer.typesetting
            for paragraph in ts:
                stylesUsing = {}
                BCScript.write(constants.Justification(paragraph.style.justification).name)
                for run in paragraph.runs:
                    BCScript.write(f"\n{run.text};{run.style.font_name};{round(run.style.font_size * 1.3333)};{run.style.fill_color};{run.style.stroke_color}\n\n")

                    # TODO: Convert text layers into bcscript file