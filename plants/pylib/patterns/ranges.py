import regex as re
from spacy import registry
from traiter.pylib import actions
from traiter.pylib import const as t_const
from traiter.pylib.matcher_compiler import Compiler
from traiter.pylib.patterns import common

ON_RANGE_MATCH = "plant_range_v1"

_SKIP = """ p. pg pg. page pi pi. fig fig. sheet sheets bis bis.
    sp. spp. no. no map """.split()

_DECODER = common.PATTERNS | {
    "9.9": {"TEXT": {"REGEX": t_const.FLOAT_TOKEN_RE}},
    "ambiguous": {"LOWER": {"IN": ["few", "many"]}},
    "conj": {"POS": {"IN": ["CCONJ"]}},
    "month": {"ENT_TYPE": "month"},
    "nope": {"TEXT": {"REGEX": r"^[&/°'\"]+$"}},
    "skip": {"LOWER": {"IN": _SKIP}},
    "a.": {"LOWER": {"REGEX": r"^[a-ln-wyz]\.?$"}},  # Keep meters and a cross
    "bad-leader": {"LOWER": {"REGEX": r"^[.=]$"}},
    "bad-follower": {"LOWER": {"REGEX": r"^[=:]$"}},
}

RANGE_LOW = Compiler(
    "range.low",
    on_match=ON_RANGE_MATCH,
    decoder=_DECODER,
    patterns=[
        "9.9",
        "( 9.9 -/or ) ambiguous ( -/to ambiguous )",
        "9.9 ( -/to [?] )",
    ],
    output=None,
)

RANGE_MIN_LOW = Compiler(
    "range.min.low",
    on_match=ON_RANGE_MATCH,
    decoder=_DECODER,
    patterns=[
        "( 9.9 -/or ) 9.9",
        "( 9.9 -/to ) 9.9",
    ],
    output=None,
)

RANGE_LOW_HIGH = Compiler(
    "range.low.high",
    on_match=ON_RANGE_MATCH,
    decoder=_DECODER,
    patterns=[
        "9.9 and/or 9.9",
        "9.9 -/to   9.9",
        "9 -* conj 9",
    ],
    output=None,
)

RANGE_LOW_MAX = Compiler(
    "range.low.max",
    on_match=ON_RANGE_MATCH,
    decoder=_DECODER,
    patterns=[
        "9.9 ( and/or 9.9 )",
        "9.9 ( -/to   9.9 )",
    ],
    output=None,
)

RANGE_MIN_LOW_HIGH = Compiler(
    "range.min.low.high",
    on_match=ON_RANGE_MATCH,
    decoder=_DECODER,
    patterns=[
        "( 9.9   -/or )   9.9 -/to     9.9",
        "( 9.9   -/or )   9.9 - and/or 9.9",
        "( 9.9   and/or ) 9.9   and/or 9.9",
        "  9.9 ( and/or   9.9    -/to  9.9 )",
    ],
    output=None,
)

RANGE_MIN_LOW_MAX = Compiler(
    "range.min.low.max",
    on_match=ON_RANGE_MATCH,
    decoder=_DECODER,
    patterns=[
        "( 9.9 - ) 9.9 -? ( -/to 9.9 [+]? )",
        "  9.9 -   9.9 - ( -/to 9.9 )",
        "  9.9 - and/or 9.9 -/to 9.9",
    ],
    output=None,
)

RANGE_LOW_HIGH_MAX = Compiler(
    "range.low.high.max",
    on_match=ON_RANGE_MATCH,
    decoder=_DECODER,
    patterns=[
        "9.9 ( and/or 9.9 -/or 9.9 [+]? )",
        "9.9 - 9.9   ( -/to 9.9 [+]? )",
        "9.9 - 9.9 - ( -/to 9.9 [+]? )",
        "9.9 - 9.9 - 9.9",
        "9.9 -/to 9.9 and/or 9.9",
        "9.9 - and/or 9.9 ( -/or 9.9 [+]? )",
        "9.9 and/or 9.9 ( and/or 9.9 [+]? )",
    ],
    output=None,
)

RANGE_MIN_LOW_HIGH_MAX = Compiler(
    "range.min.low.high.max",
    on_match=ON_RANGE_MATCH,
    decoder=_DECODER,
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
    output=None,
)

NOT_A_RANGE = Compiler(
    "not_a_range",
    on_match=actions.REJECT_MATCH,
    decoder=_DECODER,
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
    output=None,
)


@registry.misc(ON_RANGE_MATCH)
def on_range_match(ent):
    keys = ent.label_.split(".")[1:]

    nums = []
    for token in ent:
        nums += re.findall(r"\d*\.?\d+", token.text)

    # Reject big numbers
    if any(float(n) >= 1000.0 for n in nums):
        raise actions.RejectMatch()

    ent[0]._.data = {k: v for k, v in zip(keys, nums)}
    # ent._.data = {k: v for k, v in zip(keys, nums)}
    ent._.new_label = "range"
