from traiter.pylib import const as t_const
from traiter.pylib.matcher_compiler import Compiler

SHAPE_LOC = ["shape_term", "shape_leader", "location"]
SHAPE_WORD = ["shape_term", "shape_leader"]
TO = ["to"]
UNDERLINE = ["_"]

COMPILERS = [
    Compiler(
        label="surface",
        decoder={
            "-": {"TEXT": {"IN": t_const.DASH}},
            "surface": {"ENT_TYPE": "surface_term"},
            "surface_leader": {"ENT_TYPE": "surface_leader"},
        },
        patterns=[
            "                  surface",
            "surface_leader -? surface",
        ],
    ),
]
