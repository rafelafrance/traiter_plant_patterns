from ..patterns import term_patterns as terms

ALL_PARTS = terms.PARTS_SET.copy() | terms.SUBPART_SET.copy()

TRAIT_SKIPS = terms.PARTS + terms.SUBPARTS + terms.LOCATIONS + ["sex"]
TITLE_SKIPS = ["start", "end"]
FIELD_SKIPS = TITLE_SKIPS + ["trait", "dimensions"] + terms.PARTS + terms.SUBPARTS


def get_label(trait):
    keys = set(trait.keys())

    label = {}  # Dicts preserve order sets do not

    part_key = list(keys & terms.PARTS_SET)
    part = trait[part_key[0]] if part_key else ""
    label[" ".join(part) if isinstance(part, list) else part] = 1

    subpart_key = list(keys & terms.SUBPART_SET)
    if subpart_key:
        label[trait[subpart_key[0]]] = 1

    label[trait["trait"]] = 1

    if trait.get("sex"):
        label[trait["sex"]] = 1

    label = "_".join(label.keys())
    label = label.strip().replace(" ", "_").replace("-", "")
    label = label.removeprefix("_")
    label = label.removesuffix("_part")

    return label
