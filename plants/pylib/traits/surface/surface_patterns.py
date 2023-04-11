from traiter.pylib import const as t_const
from traiter.pylib.traits.pattern_compiler import Compiler

from .surface_action import SURFACE_MATCH


def surface_patterns():
    return [
        Compiler(
            label="surface",
            on_match=SURFACE_MATCH,
            decoder={
                "-": {"TEXT": {"IN": t_const.DASH}},
                "surface": {"ENT_TYPE": "surface"},
                "surface_leader": {"ENT_TYPE": "surface_leader"},
            },
            patterns=[
                "                  surface",
                "surface_leader -? surface",
            ],
        ),
    ]
