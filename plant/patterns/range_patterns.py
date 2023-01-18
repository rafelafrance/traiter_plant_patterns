"""Shared range patterns."""
import regex as re
from spacy import registry
from traiter import actions
from traiter import const as t_const
from traiter.patterns.matcher_patterns import MatcherPatterns

from . import common_patterns

ON_RANGE_MATCH = "mimosa.range.v1"

SKIP = """ p. pg pg. page pi pi. fig fig. sheet sheets bis bis.
    sp. spp. no. no map """.split()

DECODER = common_patterns.COMMON_PATTERNS | {
    "99.9": {"TEXT": {"REGEX": t_const.FLOAT_TOKEN_RE}},
    "ambiguous": {"LOWER": {"IN": ["few", "many"]}},
    "conj": {"POS": {"IN": ["CCONJ"]}},
    "month": {"ENT_TYPE": "month"},
    "nope": {"TEXT": {"REGEX": r"^[&/:°'\"]+$"}},
    "skip": {"LOWER": {"IN": SKIP}},
    "a.": {"LOWER": {"REGEX": r"^[a-ln-wyz]\.?$"}},  # Keep meters and a cross
    "bad-leader": {"LOWER": {"REGEX": r"^[.=]$"}},
    "bad-follower": {"LOWER": {"REGEX": r"^[=:]$"}},
}

RANGE_LOW = MatcherPatterns(
    "range.low",
    on_match=ON_RANGE_MATCH,
    decoder=DECODER,
    patterns=[
        "99.9",
        "( 99.9 -/or ) ambiguous ( -/to ambiguous )",
        "99.9 ( -/to [?] )",
    ],
)

RANGE_MIN_LOW = MatcherPatterns(
    "range.min.low",
    on_match=ON_RANGE_MATCH,
    decoder=DECODER,
    patterns=[
        "( 99.9 -/or ) 99.9",
        "( 99.9 -/to ) 99.9",
    ],
)

RANGE_LOW_HIGH = MatcherPatterns(
    "range.low.high",
    on_match=ON_RANGE_MATCH,
    decoder=DECODER,
    patterns=[
        "99.9 and/or 99.9",
        "99.9 -/to   99.9",
        "9 -* conj 9",
    ],
)

RANGE_LOW_MAX = MatcherPatterns(
    "range.low.max",
    on_match=ON_RANGE_MATCH,
    decoder=DECODER,
    patterns=[
        "99.9 ( and/or 99.9 )",
        "99.9 ( -/to   99.9 )",
    ],
)

RANGE_MIN_LOW_HIGH = MatcherPatterns(
    "range.min.low.high",
    on_match=ON_RANGE_MATCH,
    decoder=DECODER,
    patterns=[
        "( 99.9   -/or )   99.9 -/to     99.9",
        "( 99.9   -/or )   99.9 - and/or 99.9",
        "( 99.9   and/or ) 99.9   and/or 99.9",
        "  99.9 ( and/or   99.9    -/to  99.9 )",
    ],
)

RANGE_MIN_LOW_MAX = MatcherPatterns(
    "range.min.low.max",
    on_match=ON_RANGE_MATCH,
    decoder=DECODER,
    patterns=[
        "( 99.9 - ) 99.9 -? ( -/to 99.9 [+]? )",
        "  99.9 -   99.9 - ( -/to 99.9 )",
        "  99.9 - and/or 99.9 -/to 99.9",
    ],
)

RANGE_LOW_HIGH_MAX = MatcherPatterns(
    "range.low.high.max",
    on_match=ON_RANGE_MATCH,
    decoder=DECODER,
    patterns=[
        "99.9 ( and/or 99.9 -/or 99.9 [+]? )",
        "99.9 - 99.9   ( -/to 99.9 [+]? )",
        "99.9 - 99.9 - ( -/to 99.9 [+]? )",
        "99.9 - 99.9 - 99.9",
        "99.9 -/to 99.9 and/or 99.9",
        "99.9 - and/or 99.9 ( -/or 99.9 [+]? )",
        "99.9 and/or 99.9 ( and/or 99.9 [+]? )",
    ],
)

RANGE_MIN_LOW_HIGH_MAX = MatcherPatterns(
    "range.min.low.high.max",
    on_match=ON_RANGE_MATCH,
    decoder=DECODER,
    patterns=[
        "( 99.9 - ) 99.9 - 99.9 ( -/to 99.9 [+]? )",
        "( 99.9 -/or ) 99.9 - and/or 99.9 ( -/or 99.9 [+]? )",
        "( 99.9 and/or ) 99.9 - and/or 99.9 ( and/or 99.9 [+]? )",
        "99.9 - and/or 99.9 - and/or 99.9 -/to 99.9",
        "99.9 - and/or 99.9 -/to 99.9 ( -/or 99.9 [+]? )",
        "99.9 -/to 99.9 ( -/or 99.9 ) ( -/or 99.9 [+]? )",
        "99.9 99.9 -/to and/or 99.9 ( -/or 99.9 [+]? )",
        "99.9 and/or 99.9 - 99.9 ( -/or 99.9 [+]? )",
    ],
)

NOT_A_RANGE = MatcherPatterns(
    "not_a_range",
    on_match=actions.REJECT_MATCH,
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
)


@registry.misc(ON_RANGE_MATCH)
def on_range_match(ent):
    keys = ent.label_.split(".")[1:]
    nums = [t.text for t in ent if re.match(r"^[\d.]+$", t.text)]

    # Reject big numbers
    if any(float(n) >= 1000.0 for n in nums):
        raise actions.RejectMatch()

    ent._.data = {k: v for k, v in zip(keys, nums)}
    for token in ent:
        token._.data = ent._.data

    ent._.new_label = "range"
