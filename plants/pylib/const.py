import os
from pathlib import Path

from . import vocabulary as vocab

VOCAB_DIR = Path(vocab.__file__).parent
TERM_DB = VOCAB_DIR / "plant_terms.sqlite"
CHAR_DB = VOCAB_DIR / "char_sub_matrix.sqlite"

CURR_DIR = Path(os.getcwd())
IS_SUBDIR = CURR_DIR.name in ("notebooks", "experiments")
ROOT_DIR = Path("../.." if IS_SUBDIR else ".")

DATA_DIR = ROOT_DIR / "data"
TAXON_DB = DATA_DIR / "taxa.sqlite"

TITLE_SHAPES = set(""" Xxxxx Xxxx Xxx Xx X. Xx. X """.split())
UPPER_SHAPES = set(""" XXXXX XXXX XXX XX X. XX. X """.split())
NAME_SHAPES = list(TITLE_SHAPES) + list(UPPER_SHAPES)

LOWER_TAXON_RANK = """ species subspecies variety subvariety form subform """.split()
RANK2ID = {}


TOKEN_WEIGHTS = {",": 3, ";": 7, ".": 7, "with": 10, "of": 7}
REVERSE_WEIGHTS = {k: v * 2 for k, v in TOKEN_WEIGHTS.items()}
REVERSE_WEIGHTS[";"] = 9999
REVERSE_WEIGHTS["."] = 9999
