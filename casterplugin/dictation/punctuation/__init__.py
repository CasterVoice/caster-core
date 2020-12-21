from dragonfly import (MappingRule, Grammar, Key, Repeat, Choice, IntegerRef,
                       Function, Text, get_current_engine)


def double_text_punc_dict():
    return {
        "quotes":                            "\"\"",
        "thin quotes":                         "''",
        "tickris":                             "``",
        "prekris":                             "()",
        "brax":                                "[]",
        "curly":                               "{}",
        "angle":                               "<>",
    }


def _inv_dtpb():
    return {v: k for k, v in double_text_punc_dict().items()}


def text_punc_dict():
    # Insurers comma is recognized consistently with DNS/Natlink and
    # if/else statement workaround engines that do not expect punctuation
    # symbol as a command
    if get_current_engine().name == 'natlink':
        comma = "(comma | ,)"  # pylint: disable=unused-variable
    else:
        comma = "comma"  # pylint: disable=unused-variable  # noqa: F841

    _id = _inv_dtpb()
    return {
        "ace":                                                " ",
        "clamor":                                             "!",
        "chocky":                                            "\"",
        "hash tag":                                           "#",
        "Dolly":                                              "$",
        "modulo":                                             "%",
        "ampersand":                                          "&",
        "apostrophe | single quote | chicky":                 "'",
        "left " + _id["()"]:                                  "(",
        "right " + _id["()"]:                                 ")",
        "starling":                                           "*",
        "plus":                                               "+",
        "comma":                                              ",",
        "minus":                                              "-",
        "period | dot":                                       ".",
        "slash":                                              "/",
        "deckle":                                             ":",
        "semper":                                             ";",
        "[is] less than | left " + _id["<>"]:                 "<",
        "[is] less [than] [or] equal [to]":                  "<=",
        "equals":                                             "=",
        "[is] equal to":                                     "==",
        "[is] greater than | right " + _id["<>"]:             ">",
        "[is] greater [than] [or] equal [to]":               ">=",
        "questo":                                             "?",
        "(atty | at symbol)":                                 "@",
        "left " + _id["[]"]:                                  "[",
        "backslash":                                         "\\",
        "right " + _id["[]"]:                                 "]",
        "carrot":                                             "^",
        "underscore":                                         "_",
        "ticky | ((left | right) " + _id["``"] + " )":        "`",
        "left " + _id["{}"]:                                  "{",
        "pipe (sim | symbol)":                                "|",
        "right " + _id["{}"]:                                 "}",
        "tilde":                                              "~",
    }


class Punctuation(MappingRule):
    """
        Not implemented yet:
        # Append punctuation at end of line and shock
        "(tell | tau) <semi>":
            Function(navigation.next_line),
        # Append punctuation at end of line and create new line above
        "(hark | heart) <semi>":
            Function(navigation.previous_line),
    """
    mapping = {
        "[<long>] <text_punc> [<n>]":
            Text("%(long)s" + "%(text_punc)s" + "%(long)s")
            * Repeat(extra="n"),
        "<double_text_punc> [<n>]":
            Text("%(double_text_punc)s") + Key("left") * Repeat(extra="n"),
        "tabby [<n>]":
            Key("tab") * Repeat(extra="n"),
        "(back | shin) tabby [<n>]":
            Key("s-tab") * Repeat(extra="n"),
        "boom [<n>]":
            Text(", ") * Repeat(extra="n"),
        "bam [<n>]":
            Text(". ") * Repeat(extra="n"),
        "ace [<n100>]":
            Text(" ") * Repeat(extra="n100"),
    }
    extras = [
        IntegerRef("n", 0, 10),
        IntegerRef("n100", 0, 100),
        Choice(
            "long", {
                "long": " ",
            }),
        Choice(
            "text_punc", text_punc_dict()),
        Choice(
            "double_text_punc", double_text_punc_dict())
    ]
    defaults = {
        "n": 1,
        "n100": 1,
        "long": "",
    }
