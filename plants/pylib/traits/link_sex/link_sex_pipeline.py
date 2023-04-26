"""Link traits to a plant's sex.

We want to handle sexual dimorphism by linking traits to a plant's sex.
For example: "petals (1–)3–10(–12) mm (pistillate) or 5–8(–10) mm (staminate):
Should note that pistillate petals are 3-10 mm and staminate petals are 5-8 mm.
Named entity recognition (NER) must be run first.
"""
from spacy.language import Language
from traiter.pylib import const as t_const
from traiter.pylib.traits import add_pipe as add

from . import link_sex_patterns as pat


def build(nlp: Language, **kwargs):
    prev = add.link_pipe(
        nlp,
        name="link_sex",
        compiler=pat.link_sex_patterns(),
        parents=pat.LINK_SEX_PARENTS,
        children=pat.LINK_SEX_CHILDREN,
        weights=t_const.TOKEN_WEIGHTS,
        **kwargs,
    )

    return prev
