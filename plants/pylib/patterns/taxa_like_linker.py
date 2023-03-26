from traiter.pylib.matcher_patterns import MatcherPatterns
from traiter.pylib.patterns import common

_TAXON_LIKE_PARENTS = ["taxon_like"]
_TAXON_LIKE_CHILDREN = ["taxon"]

TAXON_LIKE_LINKER = MatcherPatterns(
    "taxon_like_linker",
    on_match=None,
    decoder=common.PATTERNS
    | {
        "taxon_like": {"ENT_TYPE": {"IN": _TAXON_LIKE_PARENTS}},
        "taxon": {"ENT_TYPE": {"IN": _TAXON_LIKE_CHILDREN}},
    },
    patterns=[
        "taxon      any* taxon_like",
        "taxon_like any* taxon",
    ],
    output=None,
)
