from pathlib import Path

from traiter.pylib.traits import trait_util
from traiter.pylib.traits.pattern_compiler import Compiler

RANK_CSV = Path(__file__).parent / "rank_terms.csv"

RANKS = trait_util.read_terms(RANK_CSV)
HIGHER_RANK = sorted({r["label"] for r in RANKS})

ABBREV_RE = r"^[A-Z][.,_]$"


DECODER = {
    "A.": {"TEXT": {"REGEX": ABBREV_RE}},
    "bad_prefix": {"ENT_TYPE": "bad_prefix"},
    "bad_suffix": {"ENT_TYPE": "bad_suffix"},
    "maybe": {"POS": {"IN": ["PROPN", "NOUN"]}},
    "binomial": {"ENT_TYPE": "binomial"},
    "monomial": {"ENT_TYPE": "monomial"},
    "higher_rank": {"ENT_TYPE": {"IN": HIGHER_RANK}},
    "subsp": {"ENT_TYPE": "subspecies_rank"},
    "var": {"ENT_TYPE": "variety_rank"},
    "subvar": {"ENT_TYPE": "subvariety_rank"},
    "f.": {"ENT_TYPE": "form_rank"},
    "subf": {"ENT_TYPE": "subform_rank"},
    "species_rank": {"ENT_TYPE": "species_rank"},
}


TAXON_COMPILERS = [
    Compiler(
        "taxon.singleton",
        decoder=DECODER,
        patterns=[
            "monomial",
            "higher_rank  monomial",
            "species_rank monomial",
        ],
    ),
]
