from traiter.pylib import const as t_const
from traiter.pylib.traits.pattern_compiler import Compiler

from ..part.pattern_compilers import PART_LABELS

# ####################################################################################
NOT_COUNT_WORDS = (
    t_const.CROSS
    + t_const.SLASH
    + """ average side times days weeks by table """.split()
)
NOT_COUNT_ENTS = """ imperial_length metric_mass imperial_mass """.split()
NOT_COUNT_PREFIX = """ chapter figure fig nos no # sec sec. """.split()
EVERY = """ every per each or more """.split()

DECODER = {
    "!": {"TEXT": "!"},
    "(": {"TEXT": {"IN": t_const.OPEN}},
    ")": {"TEXT": {"IN": t_const.CLOSE}},
    "-": {"TEXT": {"IN": t_const.DASH}},
    "/": {"TEXT": {"IN": t_const.SLASH}},
    ":": {"TEXT": {"IN": t_const.COLON}},
    ";": {"TEXT": {"IN": t_const.SEMICOLON}},
    "9": {"IS_DIGIT": True},
    "99-99": {"ENT_TYPE": "range", "OP": "+"},
    "=": {"TEXT": {"IN": ["=", ":"]}},
    "[.,]": {"LOWER": {"IN": t_const.COMMA + t_const.DOT}},
    "adp": {"POS": {"IN": ["ADP"]}},
    "any": {},
    "as": {"LOWER": {"IN": ["as"]}},
    "count_word": {"ENT_TYPE": "count_word"},
    "dim": {"ENT_TYPE": "dim"},
    "every": {"LOWER": {"IN": EVERY}},
    "no_ws": {"SPACY": False},
    "not_count_ent": {"ENT_TYPE": {"IN": NOT_COUNT_ENTS}},
    "not_count_prefix": {"LOWER": {"IN": NOT_COUNT_PREFIX}},
    "not_count_word": {"LOWER": {"IN": NOT_COUNT_WORDS}},
    "part": {"ENT_TYPE": {"IN": PART_LABELS}},
    "per_count": {"ENT_TYPE": "per_count"},
    "x": {"LOWER": "x"},
    "°": {"TEXT": "°"},
}


COMPILERS = [
    Compiler(
        label="count",
        id="count",
        decoder=DECODER,
        patterns=[
            "99-99",
            "99-99 -* per_count+",
            "( 99-99 ) per_count+",
            "99-99 -* every+ part per_count*",
            "( 99-99 ) every part",
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
            "not_count_prefix [.,]? 99-99",
            "99-99 not_count_ent",
            "99-99 not_count_word 99-99? not_count_ent?",
            "9 / 9",
            "x =? 99-99",
            "99-99 ; 99-99",
            "99-99 :",
            "99-99 any? any? any? as dim",
            "99-99 °",
            "! -? 9",
            "no_ws - 9",
        ],
    ),
]
