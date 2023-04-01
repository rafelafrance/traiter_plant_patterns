from dataclasses import dataclass

from spacy import Language
from traiter.pylib import const as t_const
from traiter.pylib import util as t_util
from traiter.pylib.traits.base_custom_pipe import BaseCustomPipe

CUSTOM_PIPE_SIZE = "custom_pipe_size"
CROSS = t_const.CROSS + t_const.COMMA


@dataclass()
class Dim:
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
    units_replace: dict[str, str]
    units_labels: list[str]
    factors_cm: dict[str, float]

    def __call__(self, doc):
        for ent in [e for e in doc.ents if e.label_ == self.trait]:
            if ent.id_ == "size.double_dim":
                ...
            elif ent.id_ == "size.high_only":
                ...
            else:
                # Put the token data into structures
                dims = [Dim(range={}, units="", dim="", about=False, sex="")]
                for token in ent:
                    if token._.data and token._.flag == "range":
                        dims[-1].range = token._.data
                    elif token._.term in self.units_labels:
                        dims[-1].units = self.replace.get(token.lower_, token.lower_)
                    elif token._.term == "dim":
                        dims[-1].dim = self.replace.get(token.lower_, token.lower_)
                    elif token._.term in ("about", "quest"):
                        dims[-1].about = True
                    elif token._.term == "sex":
                        dims[-1].sex = self.replace.get(token.lower_, token.lower_)
                    elif token.lower_ in CROSS:
                        new = Dim(range={}, units="", dim="", about=False, sex="")
                        dims.append(new)

                # Fill units
                default_units = next(d.units for d in dims if d.units)
                for dim in dims:
                    dim.units = dim.units if dim.units else default_units

                # Fill dimensions
                defaults = ["length", "width", "thickness"]
                used = [d.dim for d in dims if d.dim]
                defaults = [d for d in defaults if d not in used]
                for dim in dims:
                    dim.dim = dim.dim if dim.dim else defaults.pop(0)

                # Build the trait
                if sex := [d.sex for d in dims if d.sex]:
                    ent._.data["sex"] = sex[0]
                if any(d.about for d in dims):
                    ent._.data["uncertain"] = True
                for dim in dims:
                    for key, value in dim.range.items():
                        key = f"{dim.dim}_{key}"
                        factor = self.factors_cm[dim.units]
                        value = t_util.to_positive_float(value)
                        value = round(value * factor, 3)
                        ent._.data[key] = value

        return doc
