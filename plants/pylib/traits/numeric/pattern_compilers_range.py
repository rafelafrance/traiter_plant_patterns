from traiter.pylib import const as t_const
from traiter.pylib.traits.pattern_compiler import Compiler

AND = ["&", "and", "et"]
CONJ = AND + ["or"]
TO = ["to"]

DECODER = {
    "(": {"TEXT": {"IN": t_const.OPEN}},
    ")": {"TEXT": {"IN": t_const.CLOSE}},
    ",": {"TEXT": {"IN": t_const.COMMA}},
    "-": {"TEXT": {"IN": t_const.DASH}, "OP": "+"},
    "-/or": {"LOWER": {"IN": t_const.DASH + TO + CONJ + ["_"]}, "OP": "+"},
    "-/to": {"LOWER": {"IN": t_const.DASH + TO + ["_"]}, "OP": "+"},
    "9": {"IS_DIGIT": True},
    "9.9": {"TEXT": {"REGEX": t_const.FLOAT_TOKEN_RE}},
    "[+]": {"TEXT": {"IN": t_const.PLUS}},
    "[?]": {"TEXT": {"IN": t_const.Q_MARK}},
    "a.": {"LOWER": {"REGEX": r"^[a-ln-wyz]\.?$"}},  # Keep meters and a cross
    "ambiguous": {"LOWER": {"IN": ["few", "many"]}},
    "and/or": {"LOWER": {"IN": CONJ}},
    "bad-follower": {"LOWER": {"REGEX": r"^[=:]$"}},
    "bad-leader": {"LOWER": {"REGEX": r"^[.=]$"}},
    "conj": {"POS": {"IN": ["CCONJ"]}},
    "month": {"ENT_TYPE": "month"},
    "nope": {"TEXT": {"REGEX": r"^[&/°'\"]+$"}},
    "skip": {"ENT_TYPE": "bad_numeric"},
}

COMPILERS = [
    Compiler(
        label="range",
        id="range.low",
        decoder=DECODER,
        patterns=[
            "9.9",
            "( 9.9 -/or ) ambiguous ( -/to ambiguous )",
            "9.9 ( -/to [?] )",
        ],
    ),
    Compiler(
        label="range",
        id="range.min.low",
        decoder=DECODER,
        patterns=[
            "( 9.9 -/or ) 9.9",
            "( 9.9 -/to ) 9.9",
        ],
    ),
    Compiler(
        label="range",
        id="range.low.high",
        decoder=DECODER,
        patterns=[
            "9.9 and/or 9.9",
            "9.9 -/to   9.9",
            "9 -* conj 9",
        ],
    ),
    Compiler(
        label="range",
        id="range.low.max",
        decoder=DECODER,
        patterns=[
            "9.9 ( and/or 9.9 )",
            "9.9 ( -/to   9.9 )",
        ],
    ),
    Compiler(
        label="range",
        id="range.min.low.high",
        decoder=DECODER,
        patterns=[
            "( 9.9   -/or )   9.9 -/to     9.9",
            "( 9.9   -/or )   9.9 - and/or 9.9",
            "( 9.9   and/or ) 9.9   and/or 9.9",
            "  9.9 ( and/or   9.9    -/to  9.9 )",
        ],
    ),
    Compiler(
        label="range",
        id="range.min.low.max",
        decoder=DECODER,
        patterns=[
            "( 9.9 - ) 9.9 -? ( -/to 9.9 [+]? )",
            "  9.9 -   9.9 - ( -/to 9.9 )",
            "  9.9 - and/or 9.9 -/to 9.9",
        ],
    ),
    Compiler(
        label="range",
        id="range.low.high.max",
        decoder=DECODER,
        patterns=[
            "9.9 ( and/or 9.9 -/or 9.9 [+]? )",
            "9.9 - 9.9   ( -/to 9.9 [+]? )",
            "9.9 - 9.9 - ( -/to 9.9 [+]? )",
            "9.9 - 9.9 - 9.9",
            "9.9 -/to 9.9 and/or 9.9",
            "9.9 - and/or 9.9 ( -/or 9.9 [+]? )",
            "9.9 and/or 9.9 ( and/or 9.9 [+]? )",
        ],
    ),
    Compiler(
        label="range",
        id="range.min.low.high.max",
        decoder=DECODER,
        patterns=[
            "( 9.9 - ) 9.9 - 9.9 ( -/to 9.9 [+]? )",
            "( 9.9 -/or ) 9.9 - and/or 9.9 ( -/or 9.9 [+]? )",
            "( 9.9 and/or ) 9.9 - and/or 9.9 ( and/or 9.9 [+]? )",
            "9.9 - and/or 9.9 - and/or 9.9 -/to 9.9",
            "9.9 - and/or 9.9 -/to 9.9 ( -/or 9.9 [+]? )",
            "9.9 -/to 9.9 ( -/or 9.9 ) ( -/or 9.9 [+]? )",
            "9.9 9.9 -/to and/or 9.9 ( -/or 9.9 [+]? )",
            "9.9 and/or 9.9 - 9.9 ( -/or 9.9 [+]? )",
        ],
    ),
    Compiler(
        label="not_a_range",
        decoder=DECODER,
        patterns=[
            "9 nope",
            "  nope 9",
            "9 nope 9",
            "  nope 9 - 9",
            "9 month",
            "  month 9",
            "9 skip",
            "  skip 9",
            "  skip 9 , 9",
            "9 a.",
            "bad-leader 9",
            "9 bad-follower",
        ],
    ),
]
