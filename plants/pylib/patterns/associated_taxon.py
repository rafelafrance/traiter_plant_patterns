from traiter.pylib.pattern_compilers.matcher import Compiler

ASSOC_TAXA = Compiler(
    "associated_taxa",
    decoder={
        "assoc": {"LOWER": {"IN": ["associated", "assoc"]}},
        "label": {"LOWER": {"IN": ["species", "taxa", "taxon"]}},
    },
    patterns=[
        "assoc label",
    ],
)
