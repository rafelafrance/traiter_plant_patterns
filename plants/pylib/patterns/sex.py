from spacy import registry
from traiter.pylib.pattern_compilers.matcher import Compiler

from .terms import PLANT_TERMS

SEX = Compiler(
    "sex",
    on_match="plant_sex_v1",
    decoder={"sex": {"ENT_TYPE": "sex"}},
    patterns=["sex"],
)


@registry.misc(SEX.on_match)
def on_sex_match(ent):
    lower = ent.text.lower()
    ent._.data["sex"] = PLANT_TERMS.replace.get(lower, lower)
