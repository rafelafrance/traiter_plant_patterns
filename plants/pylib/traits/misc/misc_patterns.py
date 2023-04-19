from traiter.pylib import const as t_const
from traiter.pylib.traits.pattern_compiler import Compiler

from . import misc_action as act


def misc_patterns():
    return [
        Compiler(
            label="misc",
            on_match=act.MISC_MATCH,
            decoder={
                "(": {"TEXT": {"IN": t_const.OPEN}},
                ")": {"TEXT": {"IN": t_const.CLOSE}},
                "term": {"ENT_TYPE": {"IN": act.LABELS}},
            },
            patterns=[
                "  term ",
                "( term )",
            ],
        ),
    ]
