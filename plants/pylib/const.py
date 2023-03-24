import os
from pathlib import Path

from traiter.pylib import taxon_abbrev
from traiter.pylib.term_list import TermList

from . import vocabulary as vocab

# #########################################################################
# Useful locations

VOCAB_DIR = Path(vocab.__file__).parent
TREATMENT_CSV = VOCAB_DIR / "treatments.csv"

CURR_DIR = Path(os.getcwd())
IS_SUBDIR = CURR_DIR.name in ("notebooks", "experiments")
ROOT_DIR = Path("../.." if IS_SUBDIR else ".")

DATA_DIR = ROOT_DIR / "data"

# #########################################################################
# Setup the taxon vocabulary

TAXA_VOCAB = VOCAB_DIR / "taxa.zip"
TAXON_FILE = TAXA_VOCAB

try:
    use_mock_taxa = int(os.getenv("MOCK_TAXA"))
except (TypeError, ValueError):
    use_mock_taxa = 0

if not TAXON_FILE.exists() or use_mock_taxa:
    TAXON_FILE = VOCAB_DIR / "mock_taxa.csv"

# #########################################################################
# Used for validating taxon names

MIN_TAXON_LEN = 3  # The entire taxon must be this long
MIN_TAXON_WORD_LEN = 2  # Each word in the taxon must be this long

# #########################################################################
# Groups of entities

LINKABLE_ENTS = """
    color count duration joined shape size habit habitat leaf_duration
    leaf_folding margin reproduction sex surface venation woodiness
    """.split()

LOCATION_ENTS = """ location flower_location part_as_loc subpart_as_loc """.split()

MORPHOLOGY_ENTS = """ flower_morphology plant_morphology """.split()

NO_LINK_ENTS = """ duration habit habitat leaf_duration """.split()

PART_ENTS = """
    female_flower_part flower_part fruit_part inflorescence leaf_part male_flower_part
    multiple_parts part
    """.split()
PARTS_SET = set(PART_ENTS)

PLANT_ENTS = """ plant_duration plant_habit """.split()

TAXON_ENTS = """ taxon multi_taxon """.split()

SUBPART_ENTS = """ subpart subpart_suffix """.split()
SUBPART_SET = set(SUBPART_ENTS)

ALL_PLANT_ENTS = LINKABLE_ENTS + LOCATION_ENTS + MORPHOLOGY_ENTS + NO_LINK_ENTS
ALL_PLANT_ENTS += PART_ENTS + PLANT_ENTS + SUBPART_ENTS

# #########################################################################
# Groups of terms

PLANT_TERMS = TermList().shared("labels numerics time units")
PLANT_TERMS += TermList().read(TREATMENT_CSV)
PLANT_TERMS += TermList().read(VOCAB_DIR / "ranks.csv")
PLANT_TERMS += TermList().read(VOCAB_DIR / "job_labels.csv")

ADMIN_UNIT_TERMS = TermList().shared("us_locations").drop("county_label")

TAXON_TERMS = TermList().read(TAXON_FILE)
MONOMIAL_TERMS = TAXON_TERMS.split("monomial")
BINOMIAL_TERMS = TAXON_TERMS.split("binomial")
TAXON_RANKS = TAXON_TERMS.pattern_dict("ranks")
BINOMIAL_ABBREVS = taxon_abbrev.abbreviate_binomials(BINOMIAL_TERMS)

RANK_TERMS = TermList().read(VOCAB_DIR / "ranks.csv")
RANK_ABBREV = RANK_TERMS.pattern_dict("abbrev")
RANK_LEVELS = RANK_TERMS.column_dict("label", "level")

KEEP = """ taxon_like missing_part """.split()
KEEP += ALL_PLANT_ENTS + TAXON_ENTS


def all_traits_except(removes: list[str]) -> list:
    return [t for t in ALL_PLANT_ENTS if t not in removes]
