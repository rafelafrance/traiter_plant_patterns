from traiter.pylib import const as t_const
from traiter.pylib.traits.pattern_compiler import Compiler

HABIT_COMPILERS = [
    Compiler(
        label="habit",
        decoder={
            "-": {"TEXT": {"IN": t_const.DASH}, "OP": "+"},
            "habit": {"ENT_TYPE": "habit_term"},
            "shape": {"ENT_TYPE": "shape_term"},
            "tree": {"ENT_TYPE": "habit_tree"},
        },
        patterns=[
            "habit",
            "shape -? tree",
        ],
    )
]
