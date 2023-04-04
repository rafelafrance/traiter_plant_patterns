"""Link traits to a plant's sex.

We want to handle sexual dimorphism by linking traits to a plant's sex.
For example: "petals (1–)3–10(–12) mm (pistillate) or 5–8(–10) mm (staminate):
Should note that pistillate petals are 3-10 mm and staminate petals are 5-8 mm.
Named entity recognition (NER) must be run first.
"""
from spacy import Language
from traiter.pylib import const as t_const
from traiter.pylib.traits import add_pipe as add

from . import link_sex_pattern_compilers as comp
from .link_sex_pattern_compilers import link_sex_compilers


def build(nlp: Language, **kwargs):
    prev = add.link_pipe(
        nlp,
        name="link_sex",
        compiler=link_sex_compilers(),
        parents=comp.LINK_SEX_PARENTS,
        children=comp.LINK_SEX_CHILDREN,
        weights=t_const.TOKEN_WEIGHTS,
        **kwargs,
    )

    return prev
