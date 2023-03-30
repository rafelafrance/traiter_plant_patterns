from traiter.pylib.matcher_compiler import Compiler


PARENTS = ["sex"]
CHILDREN = """
    color count duration duration flower_location flower_part fruit_part habit habitat
    inflorescence joined leaf_duration leaf_folding leaf_part location flower_morphology
    margin multiple_parts part part_as_loc plant_duration plant_morphology reproduction
    shape size subpart subpart_as_loc subpart_suffix surface venation woodiness
    """.split()

LINK_SEX = Compiler(
    "link_sex",
    decoder={
        "sex": {"ENT_TYPE": {"IN": PARENTS}},
        "trait": {"ENT_TYPE": {"IN": CHILDREN}},
        "phrase": {"LOWER": {"REGEX": r"^([^.;:]+)$"}},
    },
    patterns=[
        "trait phrase* sex",
        "sex   phrase* trait",
    ],
)
