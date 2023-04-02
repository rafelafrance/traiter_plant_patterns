from dataclasses import dataclass

from spacy import registry
from traiter.pylib import actions
from traiter.pylib import const as t_const
from traiter.pylib import util as t_util
from traiter.pylib.matcher_patterns import MatcherPatterns
from traiter.pylib.patterns import common

from ..vocabulary import terms


@dataclass()
class Dimension:
    range: dict
    units: str
    dim: str
    about: bool
    sex: str


_CROSS = t_const.CROSS + t_const.COMMA

_FACTORS = terms.PLANT_TERMS.pattern_dict("factor_cm", float)

_FOLLOW = """ dim sex """.split()
_NOT_A_SIZE = """ for below above """.split()
_SIZE_FIELDS = """ min low high max """.split()

_SWITCH_DIM = t_const.CROSS + t_const.COMMA

_LENGTHS = ["metric_length", "imperial_length"]

_DECODER = common.PATTERNS | {
    "99.9": {"TEXT": {"REGEX": t_const.FLOAT_TOKEN_RE}},
    "[?]": {"ENT_TYPE": "quest"},
    "about": {"ENT_TYPE": "about"},
    "and": {"LOWER": "and"},
    "cm": {"ENT_TYPE": {"IN": _LENGTHS}},
    "dim": {"ENT_TYPE": "dim"},
    "follow": {"ENT_TYPE": {"IN": _FOLLOW}},
    "not_size": {"LOWER": {"IN": _NOT_A_SIZE}},
    "sex": {"ENT_TYPE": "sex"},
    "x": {"LOWER": {"IN": t_const.CROSS}},
}

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
    output=["size"],
)

SIZE_HIGH_ONLY = MatcherPatterns(
    "size.high_only",
    on_match="plant_size_high_only_v1",
    decoder=_DECODER,
    patterns=[
        "to about? 99.9 [?]? cm follow*",
    ],
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
    output=None,
)


@registry.misc(SIZE.on_match)
def on_size_match(ent):
    dimensions = scan_tokens(ent)
    fill_units(dimensions)
    fill_dimensions(dimensions)
    fill_trait_data(dimensions, ent)


def fill_trait_data(dimensions, ent):
    # Build the trait data
    if sex := [d.sex for d in dimensions if d.sex]:
        ent._.data["sex"] = sex[0]
    if any(d.about for d in dimensions):
        ent._.data["uncertain"] = True
    for dim in dimensions:
        for key, value in dim.range.items():
            key = f"{dim.dim}_{key}"
            factor = _FACTORS[dim.units]
            value = t_util.to_positive_float(value)
            if value > 1000.0:
                raise actions.RejectMatch()
            value = round(value * factor, 3)
            ent._.data[key] = value


def fill_dimensions(dimensions):
    used = [d.dim for d in dimensions if d.dim]
    defaults = ["length", "width", "thickness"]
    defaults = [d for d in defaults if d not in used]
    for dim in dimensions:
        dim.dim = dim.dim if dim.dim else defaults.pop(0)


def fill_units(dimensions):
    default_units = next(d.units for d in dimensions if d.units)
    for dim in dimensions:
        dim.units = dim.units if dim.units else default_units


def scan_tokens(ent):
    dimensions = [Dimension(range={}, units="", dim="", about=False, sex="")]
    replace = terms.PLANT_TERMS.replace

    for token in ent:
        if token.ent_type_ == "range":
            dimensions[-1].range = token._.data
        elif token.ent_type_ in _LENGTHS:
            dimensions[-1].units = replace.get(token.lower_, token.lower_)
        elif token.ent_type_ == "dim":
            if word := replace.get(token.lower_):
                dimensions[-1].dim = word
        elif token.ent_type_ in ("about", "quest"):
            dimensions[-1].about = True
        elif token.ent_type_ == "sex":
            dimensions[-1].sex = replace.get(token.lower_, token.lower_)
        elif token.lower_ in _CROSS:
            new = Dimension(range={}, units="", dim="", about=False, sex="")
            dimensions.append(new)

    return dimensions


@registry.misc(SIZE_HIGH_ONLY.on_match)
def on_size_high_only_match(ent):
    dimensions = scan_tokens(ent)

    if not (value := dimensions[0].range.get("low")):
        raise actions.RejectMatch()
    dimensions[0].range = {"high": value}

    fill_units(dimensions)
    fill_dimensions(dimensions)
    fill_trait_data(dimensions, ent)
    ent._.new_label = "size"


@registry.misc(SIZE_DOUBLE_DIM.on_match)
def on_size_double_dim_match(ent):
    """Handle the case when the dimensions are doubled but values are not.

    Like: Legumes 2.8-4.5 mm high and wide
    """
    dimensions = scan_tokens(ent)

    dims = []
    for token in ent:
        if token.ent_type_ == "dim":
            dims.append(terms.PLANT_TERMS.replace.get(token.lower_, token.lower_))

    for dimension, dim in zip(dimensions, dims):
        dimension.dim = dim

    fill_units(dimensions)
    fill_dimensions(dimensions)
    fill_trait_data(dimensions, ent)
    ent._.new_label = "size"
