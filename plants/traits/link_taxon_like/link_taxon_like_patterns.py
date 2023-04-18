from traiter.traits.pattern_compiler import Compiler

TAXON_LIKE_PARENTS = ["taxon_like"]
TAXON_LIKE_CHILDREN = ["taxon"]


def link_taxon_like_patterns():
    return Compiler(
        label="link_taxon_like",
        decoder={
            "any": {},
            "taxon_like": {"ENT_TYPE": {"IN": TAXON_LIKE_PARENTS}},
            "taxon": {"ENT_TYPE": {"IN": TAXON_LIKE_CHILDREN}},
        },
        patterns=[
            "taxon      any* taxon_like",
            "taxon_like any* taxon",
        ],
    )
