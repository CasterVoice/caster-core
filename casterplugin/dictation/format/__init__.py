from dragonfly import Function, IntegerRef, Choice, MappingRule, Dictation

from . import textformat


class Format(MappingRule):

    mapping = {
        "set [<big>] format "
        "(<capitalization> <spacing> | <capitalization> | <spacing>) "
        "[(bow|bowel)]":
            Function(textformat.set_text_format),
        "clear castervoice [<big>] formatting":
            Function(textformat.clear_text_format),
        "peek [<big>] format":
            Function(textformat.peek_text_format),
        "(<capitalization> <spacing> | <capitalization> | <spacing>) "
        "[(bow|bowel)] <textnv> [brunt]":
            Function(textformat.master_format_text),
        "[<big>] format <textnv>":
            Function(textformat.prior_text_format),
        "<word_limit> [<big>] format <textnv>":
            Function(textformat.partial_format_text),
    }

    extras = [
        Choice("big", {
            "big": True,
        }),
        Choice("capitalization", {
            "yell": 1,
            "tie": 2,
            "gerrish": 3,
            "sing": 4,
            "laws": 5,
            "say": 6,
            "cop": 7,
            "slip": 8,
        }),
        Choice(
            "spacing", {
                "gum": 1,
                "gun": 1,
                "spine": 2,
                "snake": 3,
                "pebble": 4,
                "incline": 5,
                "dissent": 6,
                "descent": 6,
            }),
        Choice("word_limit", {
            "single": 1,
            "double": 2,
            "triple": 3,
            "Quadra": 4
        }),
        Dictation("textnv"),
    ]

    defaults = {
        "big": False,
        "capitalization": 0,
        "spacing": 0,
    }
