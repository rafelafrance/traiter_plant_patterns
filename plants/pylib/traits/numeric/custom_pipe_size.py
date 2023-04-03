from dataclasses import dataclass

from spacy import Language
from traiter.pylib import const as t_const
from traiter.pylib import util as t_util
from traiter.pylib.traits.base_custom_pipe import BaseCustomPipe

CUSTOM_PIPE_SIZE = "custom_pipe_size"

CROSS = t_const.CROSS + t_const.COMMA


@dataclass()
class Dimension:
    range: dict
    units: str
    dim: str
    about: bool
    sex: str


@Language.factory(CUSTOM_PIPE_SIZE)
@dataclass()
class SizePipe(BaseCustomPipe):
    trait: str
    replace: dict[str, str]
    factors_cm: dict[str, float]

    def __call__(self, doc):
        for ent in [e for e in doc.ents if e.label_ == self.trait]:

            dimensions = self.scan_tokens(ent)

            if ent.id_ == "size":
                pass
            elif ent.id_ == "size.high_only":
                dimensions[0].range = {"high": dimensions[0].range["low"]}

            elif ent.id_ == "size.double_dim":
                dims = []
                for token in ent:
                    if token._.term == "dim":
                        dims.append(self.replace.get(token.lower_, token.lower_))

                for dimension, dim in zip(dimensions, dims):
                    dimension.dim = dim

            self.fill_units(dimensions)
            self.fill_dimensions(dimensions)
            self.fill_trait_data(dimensions, ent)

        return doc

    def scan_tokens(self, ent):
        dimensions = [Dimension(range={}, units="", dim="", about=False, sex="")]

        for token in ent:
            if token._.data and token._.flag == "range":
                dimensions[-1].range = token._.data
            elif token._.term in ("metric_length", "imperial_length"):
                if word := self.replace.get(token.lower_):
                    dimensions[-1].units += word
            elif token._.term == "dim":
                if word := self.replace.get(token.lower_):
                    dimensions[-1].dim += word
            elif token._.term in ("about", "quest"):
                dimensions[-1].about = True
            elif token._.term == "sex":
                if word := self.replace.get(token.lower_):
                    dimensions[-1].sex += word
            elif token.lower_ in CROSS:
                new = Dimension(range={}, units="", dim="", about=False, sex="")
                dimensions.append(new)

        return dimensions

    @staticmethod
    def fill_units(dimensions):
        default_units = next(d.units for d in dimensions if d.units)
        for dim in dimensions:
            dim.units = dim.units if dim.units else default_units

    @staticmethod
    def fill_dimensions(dimensions):
        used = [d.dim for d in dimensions if d.dim]
        defaults = ["length", "width", "thickness"]
        defaults = [d for d in defaults if d not in used]
        for dim in dimensions:
            dim.dim = dim.dim if dim.dim else defaults.pop(0)

    def fill_trait_data(self, dimensions, ent):
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
                factor = self.factors_cm[dim.units]
                value = t_util.to_positive_float(value)
                value = round(value * factor, 3)
                ent._.data[key] = value
