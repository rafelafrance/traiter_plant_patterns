import re
from collections import deque

from spacy import registry
from traiter.pylib import actions
from traiter.pylib import const as t_const
from traiter.pylib import util as t_util
from traiter.pylib.matcher_patterns import MatcherPatterns
from traiter.pylib.patterns import common
from traiter.pylib.term_list import TermList

from .. import const

_FACTORS = const.PLANT_TERMS.pattern_dict("factor_cm", float)

_FOLLOW = """ dim sex """.split()
_NOT_A_SIZE = """ for below above """.split()
_SIZE_FIELDS = """ min low high max """.split()

_SWITCH_DIM = t_const.CROSS + t_const.COMMA

_DECODER = common.PATTERNS | {
    "99.9": {"TEXT": {"REGEX": t_const.FLOAT_TOKEN_RE}},
    "[?]": {"ENT_TYPE": "quest"},
    "about": {"ENT_TYPE": "about"},
    "and": {"LOWER": "and"},
    "cm": {"ENT_TYPE": "metric_length"},
    "dim": {"ENT_TYPE": "dim"},
    "follow": {"ENT_TYPE": {"IN": _FOLLOW}},
    "not_size": {"LOWER": {"IN": _NOT_A_SIZE}},
    "sex": {"ENT_TYPE": "sex"},
    "x": {"LOWER": {"IN": t_const.CROSS}},
}

_TERMS = const.PLANT_TERMS.shared("units")

SIZE = MatcherPatterns(
    "size",
    on_match="plant_size_v1",
    decoder=_DECODER,
    patterns=[
        "about? 99.9-99.9 cm  follow*",
        "about? 99.9-99.9 cm? follow* x to? about? 99.9-99.9 cm follow*",
        "about? 99.9-99.9 cm? follow* , to? about? 99.9-99.9 cm follow*",
        (
            "      about? 99.9-99.9 cm? follow* "
            "x to? about? 99.9-99.9 cm? follow* "
            "x to? about? 99.9-99.9 cm  follow*"
        ),
    ],
    terms=_TERMS,
    output=["size"],
)

SIZE_HIGH_ONLY = MatcherPatterns(
    "size.high_only",
    on_match="plant_size_high_only_v1",
    decoder=_DECODER,
    patterns=[
        "to about? 99.9 [?]? cm follow*",
    ],
    terms=_TERMS,
    output=["size"],
)

SIZE_DOUBLE_DIM = MatcherPatterns(
    "size.double_dim",
    on_match="plant_size_double_dim_v1",
    decoder=_DECODER,
    patterns=[
        "about? 99.9-99.9 cm  sex? ,? dim and dim",
        "about? 99.9-99.9 cm? sex? ,? 99.9-99.9 cm dim and? ,? dim",
    ],
    terms=_TERMS,
    output=["size"],
)

_NOT_A_SIZE = MatcherPatterns(
    "not_a_size",
    on_match=actions.REJECT_MATCH,
    decoder=_DECODER,
    patterns=[
        "not_size about? 99.9-99.9 cm",
        "not_size about? 99.9-99.9 cm? x about? 99.9-99.9 cm",
    ],
    terms=_TERMS,
    output=None,
)


@registry.misc(SIZE.on_match)
def on_size_match(ent):
    _size(ent)


@registry.misc(SIZE_HIGH_ONLY.on_match)
def on_size_high_only_match(ent):
    _size(ent, True)


@registry.misc(SIZE_DOUBLE_DIM.on_match)
def on_size_double_dim_match(ent):
    """Handle the case when the dimensions are doubled but values are not.

    Like: Legumes 2.8-4.5 mm high and wide
    """
    dims = [
        const.PLANT_TERMS.replace.get(t.lower_, t.lower_)
        for t in ent
        if t.ent_type_ == "dim"
    ]

    ranges = [e for e in ent.ents if e.label_ == "range"]

    all_units = [e.text.lower() for e in ent.ents if e.label_ == "metric_length"]
    all_units = all_units + [all_units[-1]] * (len(ranges) - len(all_units))

    for dim, range_, units in zip(dims, ranges, all_units):
        _size(range_, units=units)
        for key, value in range_._.data.items():
            key_parts = key.split("_")
            if key_parts[-1] in _SIZE_FIELDS:
                new_key = f"{dim}_{key_parts[-1]}"
                ent._.data[new_key] = value
            else:
                ent._.data[key] = value
    if "range" in ent._.data:
        del ent._.data["range"]

    ent._.data["dimensions"] = sorted(d for d in dims)
    ent._.new_label = "size"


def _size(ent, high_only=False, units=None):
    dims = scan_tokens(ent, high_only)
    if units:
        dims[-1]["units"] = units
    dims = fix_dimensions(dims)
    dims = fix_units(dims)
    ent._.new_label = "size"
    fill_data(dims, ent)


def scan_tokens(ent, high_only):
    dims = [{}]

    has_range = False
    for token in ent:
        label = token.ent_type_

        if label == "range":
            has_range = True
            for field in _SIZE_FIELDS:
                if field in token._.data:
                    dims[-1][field] = t_util.to_positive_float(token._.data[field])

            if high_only:
                dims[-1]["high"] = dims[-1]["low"]
                del dims[-1]["low"]

        elif label == "metric_length":
            dims[-1]["units"] = const.PLANT_TERMS.replace[token.lower_]

        elif label == "dim":
            dims[-1]["dimension"] = const.PLANT_TERMS.replace[token.lower_]

        elif label == "sex":
            dims[-1]["sex"] = re.sub(r"\W+", "", token.lower_)

        elif label in ("quest", "about"):
            dims[-1]["uncertain"] = True

        elif token.lower_ in _SWITCH_DIM:
            dims.append({})

    if not has_range:
        raise actions.RejectMatch()

    return dims


def fix_dimensions(dims):
    """Handle when width comes before length or unlabeled dimensions."""
    noted = [d for n in dims if (d := n.get("dimension"))]
    defaults = deque(d for d in ("length", "width", "thickness") if d not in noted)

    for dim in dims:
        if not dim.get("dimension"):
            dim["dimension"] = defaults.popleft()

    return dims


def fix_units(dims):
    """Fill in missing units."""
    default = [d.get("units") for d in dims][-1]

    for dim in dims:
        dim["units"] = dim.get("units", default)

    return dims


def fill_data(dims, ent):
    """Move fields into correct place & give them consistent names."""
    for dim in dims:
        dimension = dim["dimension"]

        units = dim["units"].lower()

        for field in _SIZE_FIELDS:
            if value := dim.get(field):
                key = f"{dimension}_{field}"
                factor = _FACTORS[units]
                value = round(value * factor, 3)
                ent._.data[key] = value

        if sex := dim.get("sex"):
            ent._.data["sex"] = sex

        if dim.get("uncertain"):
            ent._.data["uncertain"] = True

    dim = sorted(d["dimension"] for d in dims)
    ent._.data["dimensions"] = dim if len(dim) > 1 else dim[0]
