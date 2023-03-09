from traiter.pylib import term_reader

from .. import const

# #########################################################################
TAXA_TERMS = term_reader.read(const.TAXA_CSV)
MONOMIAL_TERMS = term_reader.take(TAXA_TERMS, "monomial")
BINOMIAL_TERMS = term_reader.take(TAXA_TERMS, "binomial")

BASIC_TERMS = term_reader.shared("colors")
BASIC_TERMS += term_reader.shared("units")
BASIC_TERMS += term_reader.shared("numerics")
BASIC_TERMS += term_reader.read(const.VOCAB_DIR / "ranks.csv")
BASIC_TERMS += term_reader.read(const.VOCAB_DIR / "treatment.csv")

BASIC_TERMS = term_reader.drop(BASIC_TERMS, "imperial_length")
BASIC_TERMS = term_reader.drop(BASIC_TERMS, "time_units")
BASIC_TERMS = term_reader.drop(BASIC_TERMS, "ordinal numeric_units roman")

REMOVE = term_reader.pattern_dict(BASIC_TERMS, "remove")
SUFFIX_TERM = term_reader.pattern_dict(BASIC_TERMS, "suffix_term")

ALL_TERMS = BASIC_TERMS + MONOMIAL_TERMS + BINOMIAL_TERMS

REPLACE = term_reader.pattern_dict(ALL_TERMS, "replace")
RANKS = term_reader.pattern_dict(ALL_TERMS, "ranks")
RANK_ABBREV = term_reader.pattern_dict(ALL_TERMS, "abbrev")


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
