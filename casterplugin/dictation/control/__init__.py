import platform

from dragonfly import (MappingRule, Key, Grammar, Repeat, Choice,
                       IntegerRef, Function)

from castervoice import Plugin


system = platform.system()
if system == "Darwin":
    JUMP_WALL = {"left": "w-left",
                 "right": "w-right",
                 "up": "w-up",
                 "down": "w-down"}
    JUMP_WORD = {"left": "a-left",
                 "right": "a-right"}
    WORD_DELETE_MODIFIER = "a"
    DELETE_DIR = {"left": "backspace",
                  "right": "delete"}
else:
    JUMP_WALL = {"left": "home",
                 "right": "end",
                 "up": "c-home",
                 "down": "c-end"}
    JUMP_WORD = {"left": "c-left",
                 "right": "c-right"}
    WORD_DELETE_MODIFIER = "c"
    DELETE_DIR = {"left": "backspace",
                  "right": "delete"}


def key_add_modifier(key_spec, modifier):
    index = key_spec.find('-')
    if index == -1:
        return "{}-{}".format(modifier, key_spec)

    return modifier + key_spec


def jump_word(horizontal_dir):
    Key(JUMP_WORD[horizontal_dir]).execute()


def delete_word(horizontal_dir):
    Key("{}-{}".format(WORD_DELETE_MODIFIER,
                       DELETE_DIR[horizontal_dir])).execute()


class Control(MappingRule):
    """
        TODO: Unimplemented:
            # Duplicate line X times
            "duple [<n50>]":
                Function(navigation.duple_keep_clipboard),



            "bird [<n500>]":
                Key("c-left:%(n500)s")),
            "firch [<n500>]":
                Key("c-right:%(n500)s")),
            "brick [<n500>]":
                Key("s-left:%(n500)s")),
            "frick [<n500>]":
                Key("s-right:%(n500)s")),
            "blitch [<n500>]":
                Key("cs-left:%(n500)s")),
            "flitch [<n500>]":
                Key("cs-right:%(n500)s")),
    """

    mapping = {
        # New line
        'shock [<n50>]':
            Key("enter") * Repeat(extra="n50"),
        # Delete next <n> characte(s)
        "deli [<n50>]":
            Key("del/5") * Repeat(extra="n50"),
        # Delete previous <n> character(s)
        "clear [<n50>]":
            Key("backspace/5:%(n50)d"),
        "splat [<horizontal_dir>] [<n10>]":
            Function(delete_word) * Repeat(extra="n10"),
        "shackle":
            Key(JUMP_WALL["left"]) + Key(key_add_modifier(JUMP_WALL["right"],
                                                          "s")),
        "<direction> [<n500>]":
            Key("%(direction)s") * Repeat(extra='n500'),
        "fly <horizontal_dir> [<n50>]":
            Function(jump_word) * Repeat(extra="n50"),
        "(lease wally | latch) [<n10>]":
            Key("{}:%(n10)s".format(JUMP_WALL["left"])),
        "(ross wally | ratch) [<n10>]":
            Key("{}:%(n10)s".format(JUMP_WALL["right"])),
        "sauce wally [<n10>]":
            Key("{}:%(n10)s".format(JUMP_WALL["up"])),
        "dunce wally [<n10>]":
            Key("{}:%(n10)s".format(JUMP_WALL["down"])),
    }
    extras = [
        IntegerRef("n10", 1, 11),
        IntegerRef("n3", 1, 4),
        IntegerRef("n50", 1, 50),
        IntegerRef("n500", 1, 500),
        Choice("horizontal_dir", {
            "(lease|left)": "left",
            "(ross|right)": "right",
        }),
        Choice("direction", {
            "(lease|left)": "left",
            "(ross|right)": "right",
            "(sauce|up)": "up",
            "(dunce|down)": "down"
        }),
    ]
    defaults = {
        "n500": 1,
        "n50": 1,
        "n10": 1,
        "n3": 1,
        "splatdir": "backspace",
    }
