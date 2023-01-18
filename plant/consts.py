import os
from pathlib import Path

CURR_DIR = Path(os.getcwd())
IS_SUBDIR = CURR_DIR.name in ("notebooks", "experiments")
ROOT_DIR = Path("../.." if IS_SUBDIR else ".")

DATA_DIR = ROOT_DIR / "data"
MOCK_DIR = ROOT_DIR / "tests" / "mock_data"

TITLE_SHAPES = set(""" Xxxxx Xxxx Xxx Xx X. Xx. X """.split())
UPPER_SHAPES = set(""" XXXXX XXXX XXX XX X. XX. X """.split())
NAME_SHAPES = list(TITLE_SHAPES) + list(UPPER_SHAPES)

LOWER_TAXON_LEVEL = """ species subspecies variety subvariety form subform """.split()

TOKEN_WEIGHTS = {",": 3, ";": 7, ".": 7, "with": 10, "of": 7}
REVERSE_WEIGHTS = {k: v * 2 for k, v in TOKEN_WEIGHTS.items()}
REVERSE_WEIGHTS[";"] = 9999
REVERSE_WEIGHTS["."] = 9999
