import psd_tools.psd.descriptor

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


def effect_handler(effects_items):
    effect_list = []
    for effect in effects_items:
        copy_of_descriptor = {}
        copy_of_descriptor["name"] = effect.name
        for key, val in effect.__dict__["descriptor"].items():
            copy_of_descriptor[key.decode()] = Descriptor_to_dickt(val)
        effect_list.append(copy_of_descriptor)
    return effect_list
