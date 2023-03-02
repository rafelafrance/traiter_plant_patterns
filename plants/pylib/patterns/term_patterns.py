import os

from traiter.pylib import term_reader
from traiter.pylib.patterns import term_patterns as terms

from .. import const

# #########################################################################
TAXA_CSV = const.VOCAB_DIR / "taxa.csv"
# Some test taxa are in a mock CSV
if not TAXA_CSV.exists() or "MOCK_TAXA" in os.environ:
    TAXA_CSV = const.VOCAB_DIR / "mock_taxa.csv"

TAXA_TERMS = term_reader.read(TAXA_CSV)
RANK_TERMS = term_reader.read(const.VOCAB_DIR / "ranks.csv")

JOB_TERMS = term_reader.read(const.VOCAB_DIR / "jobs.csv")

TREATMENT_TERMS = term_reader.read(const.VOCAB_DIR / "treatment.csv")

TERMS = terms.COLOR_TERMS
TERMS += term_reader.shared("units")
TERMS += term_reader.shared("numerics")
TERMS += TREATMENT_TERMS
TERMS += TAXA_TERMS + RANK_TERMS

TERMS = term_reader.drop(TERMS, "imperial_length")
TERMS = term_reader.drop(TERMS, "time_units")
TERMS = term_reader.drop(TERMS, "ordinal numeric_units roman")

REPLACE = term_reader.pattern_dict(TERMS, "replace")
REMOVE = term_reader.pattern_dict(TERMS, "remove")
SUFFIX_TERM = term_reader.pattern_dict(TERMS, "suffix_term")

RANK1 = term_reader.pattern_dict(TERMS, "rank1")
RANK_ABBREV = term_reader.pattern_dict(TERMS, "abbrev")


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
