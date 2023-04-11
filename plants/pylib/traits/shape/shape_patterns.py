from traiter.pylib import const as t_const
from traiter.pylib.traits.pattern_compiler import Compiler

from .shape_action import SHAPE_MATCH

SHAPE_LOC = ["shape", "shape_leader", "location"]


def shape_patterns():
    return [
        Compiler(
            label="shape",
            on_match=SHAPE_MATCH,
            decoder={
                "-": {"TEXT": {"IN": t_const.DASH}},
                "-/to": {"LOWER": {"IN": t_const.DASH + ["to", "_"]}},
                "9": {"IS_DIGIT": True},
                "angular": {"LOWER": {"IN": ["angular", "angulate"]}},
                "shape": {"ENT_TYPE": "shape"},
                "shape_leader": {"ENT_TYPE": "shape_leader"},
                "shape_loc": {"ENT_TYPE": {"IN": SHAPE_LOC}},
                "shape_word": {"ENT_TYPE": {"IN": ["shape", "shape_leader"]}},
            },
            patterns=[
                "shape_loc*   -*    shape+",
                "shape_loc*   -*    shape       -* shape+",
                "shape_leader -/to+ shape_word+ -* shape+",
                "shape_word+  -*    shape+",
                "shape_loc* 9 -     angular",
            ],
        ),
    ]
