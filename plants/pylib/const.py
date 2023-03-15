import os
from pathlib import Path

from . import vocabulary as vocab

VOCAB_DIR = Path(vocab.__file__).parent

CURR_DIR = Path(os.getcwd())
IS_SUBDIR = CURR_DIR.name in ("notebooks", "experiments")
ROOT_DIR = Path("../.." if IS_SUBDIR else ".")

DATA_DIR = ROOT_DIR / "data"

TREATMENT_CSV = VOCAB_DIR / "treatment.csv"

# #########################################################################
TAXA_VOCAB = VOCAB_DIR / "taxa.csv"
TAXA_CSV = TAXA_VOCAB

try:
    use_mock_taxa = int(os.getenv("MOCK_TAXA"))
except (TypeError, ValueError):
    use_mock_taxa = 0

if not TAXA_CSV.exists() or use_mock_taxa:
    TAXA_CSV = VOCAB_DIR / "mock_taxa.csv"

# #########################################################################
MIN_TAXON_LEN = 3
MIN_TAXON_WORD_LEN = 2
ITIS_SPECIES_ID = 220
