from spacy import registry
from traiter.pylib.pattern_compilers.matcher import Compiler
from traiter.pylib.patterns import common

ON_HABIT_MATCH = "plant_habit_v1"


TREE = """ tree trees bush bushes """.split()


HABIT = Compiler(
    "habit",
    on_match=ON_HABIT_MATCH,
    decoder=common.PATTERNS
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
