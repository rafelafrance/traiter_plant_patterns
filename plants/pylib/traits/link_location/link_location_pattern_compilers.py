from traiter.pylib.traits.pattern_compiler import Compiler


LINK_LOCATION_PART_PARENTS = (
    """ location flower_location part_as_loc part_as_distance """.split()
)
LINK_LOCATION_PART_CHILDREN = """
    color count duration duration flower_part fruit_part habit habitat
    inflorescence joined leaf_duration leaf_folding leaf_part flower_morphology
    margin multiple_parts part plant_duration plant_morphology reproduction
    shape size subpart subpart_suffix surface venation woodiness
    """.split()

LINK_LOCATION_SUBPART_PARENTS = """ subpart_as_loc part_as_distance """.split()
LINK_LOCATION_SUBPART_CHILDREN = """
    color count duration duration flower_part fruit_part habit habitat
    inflorescence joined leaf_duration leaf_folding leaf_part flower_morphology
    margin multiple_parts part plant_duration plant_morphology reproduction
    shape size subpart_suffix surface venation woodiness
    """.split()

LINK_LOCATION_PART = Compiler(
    "link_location",
    decoder={
        "location": {"ENT_TYPE": {"IN": LINK_LOCATION_PART_PARENTS}},
        "trait": {"ENT_TYPE": {"IN": LINK_LOCATION_PART_CHILDREN}},
        "clause": {"TEXT": {"NOT_IN": list(".;:,")}},
    },
    patterns=[
        "trait    clause* location",
        "location clause* trait",
    ],
)


LINK_LOCATION_SUBPART = Compiler(
    "link_location",
    decoder={
        "location": {"ENT_TYPE": {"IN": LINK_LOCATION_SUBPART_PARENTS}},
        "trait": {"ENT_TYPE": {"IN": LINK_LOCATION_SUBPART_CHILDREN}},
        "clause": {"TEXT": {"NOT_IN": list(".;:,")}},
    },
    patterns=[
        "trait    clause* location",
        "location clause* trait",
    ],
)
