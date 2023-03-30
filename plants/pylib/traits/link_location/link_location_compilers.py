from traiter.pylib.matcher_compiler import Compiler

from ..part_location.part_location_compilers import LOCATION_ENTS

PARENTS = LOCATION_ENTS
CHILDREN = """
    color count duration duration flower_part fruit_part habit habitat
    inflorescence joined leaf_duration leaf_folding leaf_part flower_morphology
    margin multiple_parts part plant_duration plant_morphology reproduction
    shape size subpart subpart_suffix surface venation woodiness
    """.split()

LINK_LOCATION = Compiler(
    "link_location",
    decoder={
        "location": {"ENT_TYPE": {"IN": PARENTS}},
        "trait": {"ENT_TYPE": {"IN": CHILDREN}},
        "clause": {"LOWER": {"REGEX": r"^([^.;:,]+)$"}},
    },
    patterns=[
        "trait    clause* location",
        "location clause* trait",
    ],
)
