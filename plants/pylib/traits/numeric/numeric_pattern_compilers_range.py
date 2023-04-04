from traiter.pylib import const as t_const
from traiter.pylib.traits.pattern_compiler import Compiler

AND = ["&", "and", "et"]
CONJ = AND + ["or"]
TO = ["to"]

NOT_NUMERIC = """
    not_numeric metric_mass imperial_mass metric_dist imperial_dist
    """.split()


def range_compilers():
    decoder = {
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
        "bad_follower": {"LOWER": {"REGEX": r"^[=:]$"}},
        "bad_leader": {"LOWER": {"REGEX": r"^[.=]$"}},
        "bad_symbol": {"TEXT": {"REGEX": r"^[&/°'\"]+$"}},
        "conj": {"POS": {"IN": ["CCONJ"]}},
        "month": {"ENT_TYPE": "month"},
        "not_numeric": {"ENT_TYPE": {"IN": NOT_NUMERIC}},
    }

    return [
        Compiler(
            label="range",
            id="range.low",
            decoder=decoder,
            patterns=[
                "9.9",
                "( 9.9 -/or ) ambiguous ( -/to ambiguous )",
                "9.9 ( -/to [?] )",
            ],
        ),
        Compiler(
            label="range",
            id="range.min.low",
            decoder=decoder,
            patterns=[
                "( 9.9 -/or ) 9.9",
                "( 9.9 -/to ) 9.9",
            ],
        ),
        Compiler(
            label="range",
            id="range.low.high",
            decoder=decoder,
            patterns=[
                "9.9 and/or 9.9",
                "9.9 -/to   9.9",
                "9 -* conj 9",
            ],
        ),
        Compiler(
            label="range",
            id="range.low.max",
            decoder=decoder,
            patterns=[
                "9.9 ( and/or 9.9 )",
                "9.9 ( -/to   9.9 )",
            ],
        ),
        Compiler(
            label="range",
            id="range.min.low.high",
            decoder=decoder,
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
            decoder=decoder,
            patterns=[
                "( 9.9 - ) 9.9 -? ( -/to 9.9 [+]? )",
                "  9.9 -   9.9 - ( -/to 9.9 )",
                "  9.9 - and/or 9.9 -/to 9.9",
            ],
        ),
        Compiler(
            label="range",
            id="range.low.high.max",
            decoder=decoder,
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
            decoder=decoder,
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
            decoder=decoder,
            patterns=[
                "9.9 bad_symbol",
                "    bad_symbol 9.9",
                "9.9 bad_symbol 9.9",
                "    bad_symbol 9.9 - 9.9",
                "9.9 month",
                "    month 9.9",
                "9.9 not_numeric",
                "    not_numeric     ,? 9.9",
                "    not_numeric 9.9 ,  9.9",
                "9   a.",
                "    bad_leader  9.9",
                "9.9 bad_follower",
            ],
        ),
    ]
