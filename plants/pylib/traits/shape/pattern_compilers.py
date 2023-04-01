from traiter.pylib import const as t_const
from traiter.pylib.traits.pattern_compiler import Compiler

SHAPE_LOC = ["shape_term", "shape_leader", "location"]
SHAPE_WORD = ["shape_term", "shape_leader"]
TO = ["to"]
UNDERLINE = ["_"]

COMPILERS = [
    Compiler(
        label="shape",
        decoder={
            "-": {"TEXT": {"IN": t_const.DASH}},
            "-/to": {"LOWER": {"IN": t_const.DASH + TO + UNDERLINE}},
            "9": {"IS_DIGIT": True},
            "angular": {"LOWER": {"IN": ["angular", "angulate"]}},
            "shape": {"ENT_TYPE": "shape_term"},
            "shape_leader": {"ENT_TYPE": "shape_leader"},
            "shape_loc": {"ENT_TYPE": {"IN": SHAPE_LOC}},
            "shape_word": {"ENT_TYPE": {"IN": SHAPE_WORD}},
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
