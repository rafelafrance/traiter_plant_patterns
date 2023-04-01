"""Link traits to a plant's sex.

We want to handle sexual dimorphism by linking traits to a plant's sex.
For example: "petals (1–)3–10(–12) mm (pistillate) or 5–8(–10) mm (staminate):
Should note that pistillate petals are 3-10 mm and staminate petals are 5-8 mm.
Named entity recognition (NER) must be run first.
"""
from pathlib import Path

from spacy import Language
from traiter.pylib import const as t_const
from traiter.pylib.traits import add_pipe as add

from . import pattern_compilers as comp
from .pattern_compilers import LINK_SEX

HERE = Path(__file__).parent
TRAIT = HERE.stem


def build(nlp: Language, **kwargs):
    prev = add.link_pipe(
        nlp,
        name=TRAIT,
        compiler=LINK_SEX,
        parents=comp.PARENTS,
        children=comp.CHILDREN,
        weights=t_const.TOKEN_WEIGHTS,
        **kwargs,
    )

    return prev
