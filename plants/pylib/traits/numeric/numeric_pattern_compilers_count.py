from traiter.pylib import const as t_const
from traiter.pylib.traits.pattern_compiler import Compiler

from ..part.part_pattern_compilers import PART_LABELS

ALL_PARTS = PART_LABELS + ["subpart"]
NOT_COUNT_SYMBOL = t_const.CROSS + t_const.SLASH
NOT_COUNT_PREFIX = """ chapter figure fig nos no # sec sec. """.split()
EVERY = """ every per each or more """.split()
NOT_NUMERIC = """
    not_numeric metric_mass imperial_mass metric_dist imperial_dist
    """.split()

DECODER = {
    "!": {"TEXT": "!"},
    "(": {"TEXT": {"IN": t_const.OPEN}},
    ")": {"TEXT": {"IN": t_const.CLOSE}},
    "-": {"TEXT": {"IN": t_const.DASH}},
    "/": {"TEXT": {"IN": t_const.SLASH}},
    "9": {"IS_DIGIT": True},
    "99-99": {"ENT_TYPE": "range", "OP": "+"},
    ":": {"TEXT": {"IN": t_const.COLON}},
    ";": {"TEXT": {"IN": t_const.SEMICOLON}},
    "=": {"TEXT": {"IN": ["=", ":"]}},
    "[.,]": {"LOWER": {"IN": t_const.COMMA + t_const.DOT}},
    "adp": {"POS": {"IN": ["ADP"]}},
    "any": {},
    "as": {"LOWER": {"IN": ["as"]}},
    "count_suffix": {"ENT_TYPE": "count_suffix"},
    "count_word": {"ENT_TYPE": {"IN": ["count_word", "number_word"]}},
    "dim": {"ENT_TYPE": "dim"},
    "every": {"LOWER": {"IN": EVERY}},
    "is_alpha": {"IS_ALPHA": True},
    "missing": {"ENT_TYPE": "missing"},
    "not_count_symbol": {"LOWER": {"IN": NOT_COUNT_SYMBOL}},
    "not_numeric": {"ENT_TYPE": {"IN": NOT_NUMERIC}},
    "part": {"ENT_TYPE": {"IN": ALL_PARTS}},
    "per_count": {"ENT_TYPE": "per_count"},
    "X": {"LOWER": "x"},
    "x": {"LOWER": {"IN": t_const.CROSS + t_const.COMMA}},
    "°": {"TEXT": "°"},
}


COUNT_COMPILERS = [
    Compiler(
        label="count",
        id="count",
        decoder=DECODER,
        patterns=[
            "  99-99",
            "  99-99 -*             per_count+",
            "( 99-99 )              per_count+",
            "  99-99 -* every+ part per_count*",
            "( 99-99 )  every  part",
            "per_count+ adp? 99-99",
        ],
    ),
    Compiler(
        label="count",
        id="count_word",
        decoder=DECODER,
        patterns=[
            "count_word",
        ],
    ),
    Compiler(
        label="count",
        id="count_suffix",
        decoder=DECODER,
        patterns=[
            "missing? 99-99 count_suffix+",
        ],
    ),
    Compiler(
        label="count",
        id="count_suffix_word",
        decoder=DECODER,
        patterns=[
            "count_word count_suffix+",
        ],
    ),
    Compiler(
        label="not_a_count",
        decoder=DECODER,
        patterns=[
            "not_numeric [.,]? 99-99",
            "9 / 9",
            "X =? 99-99",
            "99-99 ; 99-99",
            "99-99 x 99-99",
            "99-99 :",
            "99-99 any? any? any? as dim",
            "99-99 °",
            "! -? 9",
            "is_alpha - 9",
            "9  not_numeric",
        ],
    ),
]
