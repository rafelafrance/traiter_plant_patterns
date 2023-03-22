import re

from spacy import registry
from traiter.pylib import const as t_const

from . import terms

# ####################################################################################
DELETE_MISSING_PARTS = "plant_missing_parts_v1"


@registry.misc(DELETE_MISSING_PARTS)
def delete_missing_parts(ent):
    """Remove trait if it is missing both the part and subpart."""
    data = ent._.data
    has_part = set(data.keys()) & terms.PARTS_SET
    return not has_part and not data.get("subpart")


# ####################################################################################
DELETE_PAGE_NO = "plant_page_no_v1"


@registry.misc(DELETE_PAGE_NO)
def delete_page_no(ent):
    """Remove a count if it looks like a page number."""
    # Is it the last trait in the doc?
    if ent.end != len(ent.doc) - 1 or ent.doc[-1].text != ".":
        return False

    # Is it the only trait in the doc?
    if len(ent.doc.ents) == 1:
        return False

    # Are the previous 2 tokens title case?
    if (
        ent.start > 1
        and ent.doc[ent.start - 2].shape_ in t_const.TITLE_SHAPES
        and ent.doc[ent.start - 1].shape_ in t_const.TITLE_SHAPES
    ):
        return True

    # Is there a semicolon between the two traits?
    prev = ent.doc.ents[-2]
    for token in ent.doc[prev.end : ent.start]:
        if token.text in [";", ":", "."]:
            return True

    return False


# ####################################################################################
DELETE_KM = "plant_kilometers_v1"


@registry.misc(DELETE_KM)
def delete_kilometers(ent):
    """Remove size if it's in kilometers."""
    data = ent._.data
    in_km = any(v == "km" for k, v in data.items() if k.endswith("_units"))
    return in_km


# ####################################################################################
DELETE_MISSING_COUNT = "plant_delete_missing_count_v1"


@registry.misc(DELETE_MISSING_COUNT)
def delete_missing_count(ent):
    """Remove count suffix if it's missing a number."""
    data = ent._.data
    no_count = not any(k for k in data.keys() if re.search(r"_(min|low|high|max)$", k))
    return no_count


# ####################################################################################
DELETE_OTHERS = "plant_delete_others_v1"

_OF = """ of """.split()


@registry.misc(DELETE_OTHERS)
def delete_others(ent):
    """Remove "plants of ohio" etc."""
    if ent.text.lower() in ["plants"] and len(ent.doc) > ent.start + 1:
        return ent.doc[ent.start + 1].lower_ in _OF
    return False


# ####################################################################################
DELETE_WHEN = {
    "count": [DELETE_MISSING_PARTS, DELETE_PAGE_NO],
    "count_group": DELETE_MISSING_PARTS,
    "color": DELETE_MISSING_PARTS,
    "count_suffix": DELETE_MISSING_COUNT,
    "part": DELETE_OTHERS,
    "size": [DELETE_MISSING_PARTS, DELETE_KM],
}
