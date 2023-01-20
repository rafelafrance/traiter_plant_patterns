from ..patterns import term_patterns

ALL_PARTS = term_patterns.PARTS_SET.copy() | term_patterns.SUBPART_SET.copy()
DO_NOT_SHOW = term_patterns.PARTS + term_patterns.SUBPARTS + term_patterns.LOCATIONS

TITLE_SKIPS = ["start", "end", "dimensions"]
TRAIT_SKIPS = TITLE_SKIPS + ["trait"] + term_patterns.PARTS + term_patterns.SUBPARTS


def get_label(trait):
    """Format the trait's label."""
    keys = set(trait.keys())

    part_key = list(keys & term_patterns.PARTS_SET)
    part = trait[part_key[0]] if part_key else ""
    part = " ".join(part) if isinstance(part, list) else part

    subpart_key = list(keys & term_patterns.SUBPART_SET)
    subpart = trait[subpart_key[0]] if subpart_key else ""

    trait = trait["trait"] if trait["trait"] not in ALL_PARTS else ""
    label = " ".join([p for p in [part, subpart, trait] if p])
    label = label.replace(" ", "_")
    label = label.removesuffix("_part")
    return label
