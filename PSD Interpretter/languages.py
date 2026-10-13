import json, enum

langs_object: dict = json.load(open("../languageObject.json", "r", encoding="utf-8"))

lang_keys = langs_object["properties"].keys()

del langs_object

class Text(dict):
    _keys = lang_keys
    def __init__(self, valtype=int):
        for key in Text._keys:
            self[key] = valtype()
    def __setitem__(self, key, val):
        if key not in Text._keys:
            raise KeyError
        dict.__setitem__(self, key, val)

class Demographic(enum.Enum):
    SHOUNEN = 1 # 13-18 Male
    SEINEN = 2 # +18 Male
    SHOUJO = 3 # 13-18 Female
    JOSEI = 4 # +18 Female

class Age_Rating(enum.IntEnum):
    SAFE = 6
    SUGGESTIVE = 13
    EROTICA = 16
    GORE = 18

class Publication(enum.Enum):
    ONGOING = 0
    COMPLETED = 1
    HIATUS = 2
    CANCELLED = 3