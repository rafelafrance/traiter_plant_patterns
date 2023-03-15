import plants.pylib.trait_lists
from plants.pylib.patterns import term as terms

TITLE_SKIPS = ["start", "end"]
FIELD_SKIPS = TITLE_SKIPS + ["trait", "dimensions"]
FIELD_SKIPS += plants.pylib.trait_lists.PARTS + plants.pylib.trait_lists.SUBPARTS
COLUMN_SKIPS = FIELD_SKIPS + ["taxon"]
TRAIT_SKIPS = (
    plants.pylib.trait_lists.PARTS
    + plants.pylib.trait_lists.SUBPARTS
    + plants.pylib.trait_lists.LOCATIONS
    + ["sex"]
)


def get_label(trait):
    keys = set(trait.keys())

    label = {}  # Dicts preserve order sets do not

    part_key = list(keys & plants.pylib.trait_lists.PARTS_SET)
    part = trait[part_key[0]] if part_key else ""
    label[" ".join(part) if isinstance(part, list) else part] = 1

    subpart_key = list(keys & plants.pylib.trait_lists.SUBPART_SET)
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
