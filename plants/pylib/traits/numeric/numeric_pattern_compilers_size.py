from traiter.pylib import const as t_const
from traiter.pylib.traits.pattern_compiler import Compiler

SEX_DIM_ENTS = """ dim sex """.split()
LENGTH_ENTS = ["metric_length", "imperial_length"]

DECODER = {
    "99.9": {"TEXT": {"REGEX": t_const.FLOAT_TOKEN_RE}},
    "99-99": {"ENT_TYPE": "range", "OP": "+"},
    ",": {"TEXT": {"IN": t_const.COMMA}},
    "about": {"ENT_TYPE": "about"},
    "any": {},
    "and": {"LOWER": "and"},
    "cm": {"ENT_TYPE": {"IN": LENGTH_ENTS}},
    "dim": {"ENT_TYPE": "dim"},
    "in": {"LOWER": "in"},
    "sex/dim": {"ENT_TYPE": {"IN": SEX_DIM_ENTS}},
    "not_numeric": {"ENT_TYPE": "not_numeric"},
    "sex": {"ENT_TYPE": "sex"},
    "to": {"LOWER": "to"},
    "x": {"LOWER": {"IN": t_const.CROSS + t_const.COMMA}},
}

SIZE_COMPILERS = [
    Compiler(
        label="size",
        id="size",
        decoder=DECODER,
        patterns=[
            "about* 99-99                    about*       cm+ in? sex/dim*",
            "about* 99-99 cm* sex/dim* x to? about* 99-99 cm+ in? sex/dim*",
            (
                "      about* 99-99 cm* in? sex/dim* "
                "x to? about* 99-99 cm* in? sex/dim* "
                "x to? about* 99-99 cm+ in? sex/dim*"
            ),
        ],
    ),
    Compiler(
        label="size",
        id="size.high_only",
        decoder=DECODER,
        patterns=[
            "to about* 99.9 about* cm+ in? sex/dim*",
        ],
    ),
    Compiler(
        label="size",
        id="size.double_dim",
        decoder=DECODER,
        patterns=[
            "about* 99-99 cm+ sex? ,? dim+ and  dim+",
            "about* 99-99 cm* sex? ,? 99-99 cm+ dim+ and dim+",
            "about* 99-99 cm* sex? ,? 99-99 cm+ dim+ ,   dim+",
        ],
    ),
    Compiler(
        label="not_a_size",
        decoder=DECODER,
        patterns=[
            "not_numeric about* 99-99 cm+",
            "not_numeric about* 99-99 cm* x about* 99-99 cm+",
            "                   99-99 cm not_numeric",
        ],
    ),
]
