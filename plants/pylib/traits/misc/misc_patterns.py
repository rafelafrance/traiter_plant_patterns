from traiter.pylib import const as t_const
from traiter.pylib.traits.pattern_compiler import Compiler

from .misc_action import LABELS
from .misc_action import MISC_MATCH


def misc_patterns():
    return [
        Compiler(
            label="misc",
            on_match=MISC_MATCH,
            decoder={
                "(": {"TEXT": {"IN": t_const.OPEN}},
                ")": {"TEXT": {"IN": t_const.CLOSE}},
                "term": {"ENT_TYPE": {"IN": LABELS}},
            },
            patterns=[
                "  term ",
                "( term )",
            ],
        ),
    ]
