from traiter.pylib import taxon_abbrev
from traiter.pylib.term_list import TermList

from .. import const

PARTS = """
    female_flower_part flower_part fruit_part inflorescence leaf_part male_flower_part
    multiple_parts part
    """.split()
PARTS_SET = set(PARTS)

LOCATIONS = """ location flower_location part_as_loc subpart_as_loc """.split()

LINKABLE_TRAITS = """
    color color_mod count duration joined shape size habit habitat leaf_duration
    leaf_folding margin reproduction sex surface venation woodiness
    """.split()

MORPHOLOGIES = """ flower_morphology plant_morphology """.split()

PLANT_TRAITS = """ plant_duration plant_habit """.split()

TAXA = ["taxon", "multi_taxon"]

SUBPARTS = ["subpart", "subpart_suffix"]
SUBPART_SET = set(SUBPARTS)

ALL_TRAITS = LOCATIONS + MORPHOLOGIES + PARTS + PLANT_TRAITS + SUBPARTS
ALL_TRAITS += LINKABLE_TRAITS

NO_LINK = """ duration habit habitat leaf_duration """.split()


# ####################################################################################
ADMIN_UNIT_TERMS = TermList().shared("us_locations")

PLANT_TERMS = TermList().shared("labels numerics time units")
PLANT_TERMS += TermList().shared("labels").pick("about")
PLANT_TERMS += TermList().read(const.TREATMENT_CSV)
PLANT_TERMS += TermList().read(const.VOCAB_DIR / "ranks.csv")

TAXON_TERMS = TermList().read(const.TAXON_FILE)
MONOMIAL_TERMS = TAXON_TERMS.split("monomial")
BINOMIAL_TERMS = TAXON_TERMS.split("binomial")
TAXON_RANKS = TAXON_TERMS.pattern_dict("ranks")
RANK_TERMS = TermList().read(const.VOCAB_DIR / "ranks.csv")
RANK_ABBREV = RANK_TERMS.pattern_dict("abbrev")
BINOMIAL_ABBREVS = taxon_abbrev.abbreviate_binomials(BINOMIAL_TERMS)

KEEP = """ taxon_like missing_part """.split()
KEEP += ALL_TRAITS + TAXA


# ####################################################################################
def all_traits_except(removes: list[str]) -> list:
    return [t for t in ALL_TRAITS if t not in removes]
