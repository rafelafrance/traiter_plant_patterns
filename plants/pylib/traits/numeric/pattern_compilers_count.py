from traiter.pylib import const as t_const
from traiter.pylib.traits.pattern_compiler import Compiler

from ..part.pattern_compilers import PART_LABELS

# ####################################################################################
NOT_COUNT_SYMBOL = t_const.CROSS + t_const.SLASH
# NOT_COUNT_ENTS = """ metric_length imperial_length metric_mass imperial_mass """.split()
NOT_COUNT_PREFIX = """ chapter figure fig nos no # sec sec. """.split()
EVERY = """ every per each or more """.split()

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
    "count_word": {"ENT_TYPE": "count_word"},
    "dim": {"ENT_TYPE": "dim"},
    "every": {"LOWER": {"IN": EVERY}},
    "no_ws": {"SPACY": False},
    # "not_count_ent": {"ENT_TYPE": {"IN": NOT_COUNT_ENTS}},
    "not_count_symbol": {"LOWER": {"IN": NOT_COUNT_SYMBOL}},
    "not_count_word": {"ENT_TYPE": "not_count_word"},
    "part": {"ENT_TYPE": {"IN": PART_LABELS}},
    "per_count": {"ENT_TYPE": "per_count"},
    "X": {"LOWER": "x"},
    "x": {"LOWER": {"IN": t_const.CROSS + t_const.COMMA}},
    "°": {"TEXT": "°"},
}


COMPILERS = [
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
        label="not_a_count",
        decoder=DECODER,
        patterns=[
            "      not_count_word [.,]? 99-99",
            # "99-99 not_count_ent",
            # "99-99 not_count_word   99-99? not_count_ent?",
            # "99-99 not_count_symbol 99-99? not_count_ent?",
            "9 / 9",
            "X =? 99-99",
            "99-99 ; 99-99",
            "99-99 x 99-99",
            "99-99 :",
            "99-99 any? any? any? as dim",
            "99-99 °",
            "! -? 9",
            "no_ws - 9",
        ],
    ),
]
