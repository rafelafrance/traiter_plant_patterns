from ..patterns import term_patterns as terms

ALL_PARTS = terms.PARTS_SET.copy() | terms.SUBPART_SET.copy()
EXTRAS = set(""" sex location group """.split())

TRAIT_SKIPS = terms.PARTS + terms.SUBPARTS + terms.LOCATIONS
TITLE_SKIPS = ["start", "end", "dimensions"]
FIELD_SKIPS = TITLE_SKIPS + ["trait", "taxon"] + terms.PARTS + terms.SUBPARTS


def get_label(trait):
    keys = set(trait.keys())

    part_key = list(keys & terms.PARTS_SET)
    part = trait[part_key[0]] if part_key else ""
    part = " ".join(part) if isinstance(part, list) else part

    subpart_key = list(keys & terms.SUBPART_SET)
    subpart = trait[subpart_key[0]] if subpart_key else ""

    trait_type = trait["trait"] if trait["trait"] not in ALL_PARTS else ""

    extras = sorted(v for k, v in trait.items() if k in EXTRAS)

    label = "_".join([p for p in [part, subpart, trait_type] + extras if p])
    label = label.replace(" ", "_").replace("-", "")
    label = label.removesuffix("_part")
    return label
