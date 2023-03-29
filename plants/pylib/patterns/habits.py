from spacy import registry
from traiter.pylib.matcher_compiler import Compiler
from traiter.pylib.patterns import common

from ..vocabulary import terms

_TREE = """ tree trees bush bushes """.split()

HABIT = Compiler(
    "habit",
    decoder=common.PATTERNS
    | {
        "habit": {"ENT_TYPE": "plant_habit"},
        "shape": {"ENT_TYPE": "shape"},
        "tree": {"LOWER": {"IN": _TREE}},
    },
    patterns=[
        "habit",
        "shape -? tree",
    ],
)


@registry.misc(HABIT.on_match)
def on_habit_match(ent):
    ent._.new_label = "habit"
    ent._.data["trait"] = "habit"
    if "plant_habit" in ent._.data:
        habit = ent._.data["plant_habit"].lower()
        del ent._.data["plant_habit"]
    else:
        habit = ent.text.lower()
    ent._.data["habit"] = terms.PLANT_TERMS.replace.get(habit, habit)
