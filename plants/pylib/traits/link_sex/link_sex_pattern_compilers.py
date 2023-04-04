from traiter.pylib.traits.pattern_compiler import Compiler


LINK_SEX_PARENTS = ["sex"]
LINK_SEX_CHILDREN = """
    color count duration duration flower_location flower_part fruit_part habit habitat
    inflorescence joined leaf_duration leaf_folding leaf_part location flower_morphology
    margin multiple_parts part part_as_loc plant_duration plant_morphology reproduction
    shape size subpart subpart_as_loc subpart_suffix surface venation woodiness
    """.split()


def link_sex_compilers():
    return Compiler(
        "link_sex",
        decoder={
            "sex": {"ENT_TYPE": {"IN": LINK_SEX_PARENTS}},
            "trait": {"ENT_TYPE": {"IN": LINK_SEX_CHILDREN}},
            "phrase": {"TEXT": {"NOT_IN": list(".;:")}},
        },
        patterns=[
            "trait phrase* sex",
            "sex   phrase* trait",
        ],
    )
