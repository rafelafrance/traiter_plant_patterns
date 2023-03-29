from spacy import registry
from traiter.pylib.matcher_compiler import Compiler

from ..vocabulary import terms

SEX = Compiler(
    "sex",
    on_match="plant_sex_v1",
    decoder={"sex": {"ENT_TYPE": "sex"}},
    patterns=["sex"],
    output=["sex"],
)


@registry.misc(SEX.on_match)
def on_sex_match(ent):
    lower = ent.text.lower()
    ent._.data["sex"] = terms.PLANT_TERMS.replace.get(lower, lower)
