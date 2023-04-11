from traiter.pylib.traits.pattern_compiler import Compiler

from .taxon_like_action import TAXON_LABELS
from .taxon_like_action import TAXON_LIKE_MATCH


def taxon_like_patterns():
    return Compiler(
        label="taxon_like",
        on_match=TAXON_LIKE_MATCH,
        decoder={
            "any": {},
            "prep": {"POS": {"IN": ["ADP", "CCONJ"]}},
            "similar": {"ENT_TYPE": "similar"},
            "taxon": {"ENT_TYPE": {"IN": TAXON_LABELS}},
        },
        patterns=[
            "similar+ taxon+",
            "similar+ any? prep taxon+",
        ],
    )
