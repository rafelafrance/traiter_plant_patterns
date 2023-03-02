import os
from pathlib import Path

from . import vocabulary as vocab

VOCAB_DIR = Path(vocab.__file__).parent

CURR_DIR = Path(os.getcwd())
IS_SUBDIR = CURR_DIR.name in ("notebooks", "experiments")
ROOT_DIR = Path("../.." if IS_SUBDIR else ".")

DATA_DIR = ROOT_DIR / "data"
