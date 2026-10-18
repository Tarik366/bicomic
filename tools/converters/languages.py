import json, enum

langs_object: dict = json.load(open("../languageObject.json", "r", encoding="utf-8"))

lang_keys = langs_object["properties"].keys()

del langs_object

class Text(dict):
    _keys = lang_keys
    
    def __init__(self, dict = {}, /, **kwds):
        for key, word in dict.items():
            self[key.lower()] = word
        for key, word in kwds.items():
            self[key.lower()] = word

    def __setitem__(self, key, val):
        if key not in Text._keys:
            raise KeyError
        dict.__setitem__(self, key, val)

class Demographic(enum.Enum):
    SHOUNEN = 1 # 13-18 Male
    SEINEN = 2 # +18 Male
    SHOUJO = 3 # 13-18 Female
    JOSEI = 4 # +18 Female

class Format(enum.Enum):
    KOMA4 = 0
    ADAPTATION = 1
    ANTHOLOGY = 2
    AWARD_WINNING = 3
    DOUJINSHI = 4
    FAN_COLORED = 5
    FULL_COLORED = 6
    LONG_STRIP = 7
    OFFICIAL_COLORED = 8
    ONESHOT = 9
    SELF_PUBLISHED = 10
    WEB_COMIC = 11

class Age_Rating(enum.IntEnum):
# This keys are for mangadex-like rating tags, use actual age number as you can
    SAFE = 6
    SUGGESTIVE = 13
    EROTICA = 16
    GORE = 18

class Publication(enum.Enum):
    ONGOING = 0
    COMPLETED = 1
    HIATUS = 2
    CANCELLED = 