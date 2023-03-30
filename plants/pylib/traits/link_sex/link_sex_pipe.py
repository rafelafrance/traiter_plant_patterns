"""Link traits to a plant's sex.

We want to handle sexual dimorphism by linking traits to a plant's sex.
For example: "petals (1–)3–10(–12) mm (pistillate) or 5–8(–10) mm (staminate):
Should note that pistillate petals are 3-10 mm and staminate petals are 5-8 mm.
Named entity recognition (NER) must be run first.
"""
from pathlib import Path

from spacy import Language
from traiter.pylib import add_pipe as add
from traiter.pylib import const as t_const
from traiter.pylib import trait_util

from . import link_sex_compilers as comp

HERE = Path(__file__).parent
TRAIT = HERE.stem


def pipe(nlp: Language, **kwargs):
    patterns = trait_util.get_patterns(HERE / f"{TRAIT}_patterns.jsonl")
    prev = add.link_pipe(
        nlp,
        patterns,
        name=TRAIT,
        parents=comp.PARENTS,
        children=comp.CHILDREN,
        weights=t_const.TOKEN_WEIGHTS,
        **kwargs,
    )

    return prev
