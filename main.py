from psd_tools import PSDImage, constants, color_convert

psd = PSDImage.open('test.psd')
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

with open("export.bcs","w") as BCScript:

    # list of fonts in the psd file for font gathering process
    fontset = []

    for layer in psd:
        if layer.kind == "type":
            print(f"{layer.size}, {layer.offset}")
            print(layer.text)

            text = layer.engine_dict['Editor']['Text'].value

            ts = layer.typesetting
            for paragraph in ts:
                stylesUsing = {}
                print(constants.Justification(paragraph.style.justification).name)
                for run in paragraph.runs:
                    print(run.text, run.style.font_name, f"{round(run.style.font_size * 1.3333)}px", run.style.fill_color, run.style.stroke_color)

                    # TODO: Convert text layers into bcscript file