from traiter.pylib.patterns import term_patterns as terms
from traiter.pylib.terms.db import Db

from .. import const

# #########################################################################
# TERMS = Db.shared("colors units time numerics")
TERMS = terms.COLOR_TERMS + terms.UNIT_TERMS + terms.TIME_TERMS + terms.NUMERIC_TERMS
TERMS += Db.select_term_set(const.TERM_DB, "plant_treatment")
TERMS += Db.trailing_dash(TERMS, label="color")
TERMS += Db.select_term_set(const.TAXON_DB, "taxa")
TERMS += Db.select_term_set(const.TAXON_DB, "ranks")
TERMS.drop("imperial_length")
TERMS.drop("time_units")
TERMS.drop("ordinal numeric_units roman")

REPLACE = TERMS.pattern_dict("replace")
REMOVE = TERMS.pattern_dict("remove")
SUFFIX_TERM = TERMS.pattern_dict("suffix_term")

RANK1 = TERMS.pattern_dict("rank1")
RANK_ABBREV = TERMS.pattern_dict("abbrev")


# #########################################################################
PARTS = """
    female_flower_part
    flower_part
    fruit_part
    inflorescence
    leaf_part
    male_flower_part
    multiple_parts
    part
    """.split()
PARTS_SET = set(PARTS)

LOCATIONS = """ location flower_location part_as_loc subpart_as_loc """.split()
MORPHOLOGIES = """ flower_morphology plant_morphology """.split()
PLANT_TRAITS = """ plant_duration plant_habit """.split()
TAXA = ["taxon", "multi_taxon"]

SUBPARTS = ["subpart", "subpart_suffix"]
SUBPART_SET = set(SUBPARTS)

TRAITS = """
    color
    color_mod
    count
    duration
    joined
    shape
    size
    habit
    habitat
    leaf_duration
    leaf_folding
    margin
    reproduction
    sex
    surface
    venation
    woodiness
""".split()
TRAITS_SET = set(TRAITS)

ALL_TRAITS = LOCATIONS + MORPHOLOGIES + PARTS + PLANT_TRAITS + SUBPARTS + TRAITS
ALL_TRAITS_SET = set(ALL_TRAITS)

NO_LINK = """ duration habit habitat leaf_duration """.split()


def all_traits_except(removes: list[str]) -> list:
    return [t for t in ALL_TRAITS if t not in removes]
