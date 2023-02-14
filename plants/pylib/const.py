import os
from pathlib import Path

from . import vocabulary as vocab

VOCAB_DIR = Path(vocab.__file__).parent
TERM_DB = VOCAB_DIR / "plant_terms.sqlite"
CHAR_DB = VOCAB_DIR / "char_sub_matrix.sqlite"

FULL_TAXON_DB = (VOCAB_DIR / "taxa.sqlite").absolute()
# Some test taxa are in the term DB
TAXON_DB = FULL_TAXON_DB if FULL_TAXON_DB.exists() else TERM_DB

CURR_DIR = Path(os.getcwd())
IS_SUBDIR = CURR_DIR.name in ("notebooks", "experiments")
ROOT_DIR = Path("../.." if IS_SUBDIR else ".")

DATA_DIR = ROOT_DIR / "data"

TITLE_SHAPES = set(""" Xxxxx Xxxx Xxx Xx X. Xx. X """.split())
UPPER_SHAPES = set(""" XXXXX XXXX XXX XX X. XX. X """.split())
NAME_SHAPES = list(TITLE_SHAPES) + list(UPPER_SHAPES)

TOKEN_WEIGHTS = {",": 3, ";": 7, ".": 7, "with": 10, "of": 7}
REVERSE_WEIGHTS = {k: v * 2 for k, v in TOKEN_WEIGHTS.items()}
REVERSE_WEIGHTS[";"] = 9999
REVERSE_WEIGHTS["."] = 9999

ITIS_SPECIES_ID = 220
