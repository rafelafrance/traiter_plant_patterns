from traiter.pylib import const as t_const
from traiter.pylib.pipes.reject_match import REJECT_MATCH
from traiter.pylib.traits.pattern_compiler import Compiler

from .numeric_action_size import SIZE_DOUBLE_DIM_MATCH
from .numeric_action_size import SIZE_HIGH_ONLY_MATCH
from .numeric_action_size import SIZE_MATCH


def size_patterns():
    decoder = {
        "99.9": {"TEXT": {"REGEX": t_const.FLOAT_TOKEN_RE}},
        "99-99": {"ENT_TYPE": "range", "OP": "+"},
        ",": {"TEXT": {"IN": t_const.COMMA}},
        "about": {"ENT_TYPE": "about"},
        "any": {},
        "and": {"LOWER": "and"},
        "cm": {"ENT_TYPE": {"IN": ["metric_length", "imperial_length"]}},
        "dim": {"ENT_TYPE": "dim"},
        "in": {"LOWER": "in"},
        "sex/dim": {"ENT_TYPE": {"IN": ["dim", "sex"]}},
        "not_numeric": {"ENT_TYPE": "not_numeric"},
        "sex": {"ENT_TYPE": "sex"},
        "to": {"LOWER": "to"},
        "x": {"LOWER": {"IN": t_const.CROSS + t_const.COMMA}},
    }

    return [
        Compiler(
            label="size",
            id="size",
            on_match=SIZE_MATCH,
            decoder=decoder,
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
            label="size.high_only",
            id="size",
            on_match=SIZE_HIGH_ONLY_MATCH,
            decoder=decoder,
            patterns=[
                "to about* 99.9 about* cm+ in? sex/dim*",
            ],
        ),
        Compiler(
            label="size.double_dim",
            id="size",
            on_match=SIZE_DOUBLE_DIM_MATCH,
            decoder=decoder,
            patterns=[
                "about* 99-99 cm+ sex? ,? dim+ and  dim+",
                "about* 99-99 cm* sex? ,? 99-99 cm+ dim+ and dim+",
                "about* 99-99 cm* sex? ,? 99-99 cm+ dim+ ,   dim+",
            ],
        ),
        Compiler(
            label="not_a_size",
            on_match=REJECT_MATCH,
            decoder=decoder,
            patterns=[
                "not_numeric about* 99-99 cm+",
                "not_numeric about* 99-99 cm* x about* 99-99 cm+",
                "                   99-99 cm not_numeric",
            ],
        ),
    ]
