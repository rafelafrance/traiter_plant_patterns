from spacy import registry
from traiter.pylib.matcher_patterns import MatcherPatterns
from traiter.pylib.patterns import common

from ..vocabulary import terms

_TREE = """ tree trees bush bushes """.split()

HABIT = MatcherPatterns(
    "habit",
    on_match="plant_habit_v1",
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
    output=["habit"],
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
