from spacy import registry
from traiter.pylib.matcher_patterns import MatcherPatterns

from .. import const

SEX = MatcherPatterns(
    "sex",
    on_match="plant_sex_v1",
    decoder={"sex": {"ENT_TYPE": "sex"}},
    patterns=["sex"],
    terms=const.PLANT_TERMS,
    keep=["sex"],
)


@registry.misc(SEX.on_match)
def on_sex_match(ent):
    lower = ent.text.lower()
    ent._.data["sex"] = const.PLANT_TERMS.replace.get(lower, lower)
