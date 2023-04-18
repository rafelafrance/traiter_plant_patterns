from dataclasses import dataclass

from spacy import registry
from traiter.pylib import const as t_const
from traiter.pylib import util as t_util
from traiter.traits import trait_util

from .range_action import ALL_CSVS
from .range_action import REPLACE

SIZE_MATCH = "size_match"
SIZE_HIGH_ONLY_MATCH = "size_high_only_match"
SIZE_DOUBLE_DIM_MATCH = "size_double_dim_match"

FACTORS_CM = trait_util.term_data(ALL_CSVS, "factor_cm", float)

CROSS = t_const.CROSS + t_const.COMMA


@dataclass()
class Dimension:
    range: dict
    units: str
    dim: str
    about: bool
    sex: str


@registry.misc(SIZE_MATCH)
def size_match(ent):
    dimensions = scan_tokens(ent)
    fill_units(dimensions)
    fill_dimensions(dimensions)
    fill_trait_data(dimensions, ent)


@registry.misc(SIZE_HIGH_ONLY_MATCH)
def size_high_only_match(ent):
    dimensions = scan_tokens(ent)
    dimensions[0].range = {"high": dimensions[0].range["low"]}
    fill_units(dimensions)
    fill_dimensions(dimensions)
    fill_trait_data(dimensions, ent)


@registry.misc(SIZE_DOUBLE_DIM_MATCH)
def size_double_dim_match(ent):
    dimensions = scan_tokens(ent)

    dims = []
    for token in ent:
        if token._.term == "dim":
            dims.append(REPLACE.get(token.lower_, token.lower_))

    for dimension, dim in zip(dimensions, dims):
        dimension.dim = dim

    fill_units(dimensions)
    fill_dimensions(dimensions)
    fill_trait_data(dimensions, ent)


def scan_tokens(ent):
    dimensions = [Dimension(range={}, units="", dim="", about=False, sex="")]

    for token in ent:
        if token._.flag == "range_data":
            dimensions[-1].range = token._.data
        elif token._.term in ("metric_length", "imperial_length"):
            if word := REPLACE.get(token.lower_):
                dimensions[-1].units += word
        elif token._.term == "dim":
            if word := REPLACE.get(token.lower_):
                if word not in ("in",):
                    dimensions[-1].dim += word
        elif token._.term in ("about", "quest"):
            dimensions[-1].about = True
        elif token._.term == "sex":
            if word := REPLACE.get(token.lower_):
                dimensions[-1].sex += word
        elif token.lower_ in CROSS:
            new = Dimension(range={}, units="", dim="", about=False, sex="")
            dimensions.append(new)

    return dimensions


def fill_units(dimensions):
    default_units = next(d.units for d in dimensions if d.units)
    for dim in dimensions:
        dim.units = dim.units if dim.units else default_units


def fill_dimensions(dimensions):
    used = [d.dim for d in dimensions if d.dim]
    defaults = ["length", "width", "thickness"]
    defaults = [d for d in defaults if d not in used]
    for dim in dimensions:
        dim.dim = dim.dim if dim.dim else defaults.pop(0)


def fill_trait_data(dimensions, ent):
    ent._.data["units"] = "cm"
    if sex := [d.sex for d in dimensions if d.sex]:
        ent._.data["sex"] = sex[0]
    if any(d.about for d in dimensions):
        ent._.data["uncertain"] = True

    # "dimensions" is used to link traits
    dims = sorted(d.dim for d in dimensions)
    ent._.data["dimensions"] = dims if len(dims) > 1 else dims[0]

    # Build the key and value for the range's: min, low, high, max
    for dim in dimensions:
        for key, value in dim.range.items():
            key = f"{dim.dim}_{key}"
            factor = FACTORS_CM[dim.units]
            value = t_util.to_positive_float(value)
            value = round(value * factor, 3)
            ent._.data[key] = value
