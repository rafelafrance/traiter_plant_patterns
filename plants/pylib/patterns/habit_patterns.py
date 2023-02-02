from spacy import registry
from traiter.pylib.patterns.matcher_patterns import MatcherPatterns

from . import common_patterns

ON_HABIT_MATCH = "plant_habit_v1"


TREE = """ tree trees bush bushes """.split()


HABIT = MatcherPatterns(
    "habit",
    on_match=ON_HABIT_MATCH,
    decoder=common_patterns.COMMON_PATTERNS
    | {
        "habit": {"ENT_TYPE": "plant_habit"},
        "shape": {"ENT_TYPE": "shape"},
        "tree": {"LOWER": {"IN": TREE}},
    },
    patterns=[
        "habit",
        "shape -? tree",
    ],
)


@registry.misc(ON_HABIT_MATCH)
def on_habit_match(ent):
    ent._.new_label = "habit"
    ent._.data["trait"] = "habit"
    if "plant_habit" in ent._.data:
        ent._.data["habit"] = ent._.data["plant_habit"]
        del ent._.data["plant_habit"]
    else:
        ent._.data["habit"] = ent.text.lower()
