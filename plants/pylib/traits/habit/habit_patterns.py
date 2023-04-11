from traiter.pylib import const as t_const
from traiter.pylib.traits.pattern_compiler import Compiler

from . import habit_action as act


def habit_compilers():
    return [
        Compiler(
            label="habit",
            on_match=act.HABIT_MATCH,
            decoder={
                "-": {"TEXT": {"IN": t_const.DASH}, "OP": "+"},
                "habit": {"ENT_TYPE": "habit"},
                "shape": {"ENT_TYPE": "shape"},
                "tree": {"ENT_TYPE": "habit_tree"},
            },
            patterns=[
                "habit",
                "shape -? tree",
            ],
        )
    ]
