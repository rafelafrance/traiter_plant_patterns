import re

from spacy import registry
from traiter.pylib import const as t_const

import plants.pylib.trait_lists

PARTIAL_TRAITS = """ about authority bad_taxon color_mod cross dim dimension
    imperial_length imperial_mass joined length_units rank margin_leader metric_length
    metric_mass month not_a_range number_word per_count plant_taxon quest range
    shape_leader shape_suffix skip units surface_leader elev_label no_label
    class_rank division_rank family_rank genus_rank infraclass_rank infradivision_rank
    infrakingdom_rank kingdom_rank order_rank section_rank series_rank subclass_rank
    subdivision_rank subfamily_rank subgenus_rank subkingdom_rank suborder_rank
    subsection_rank subseries_rank subtribe_rank superclass_rank superdivision_rank
    superorder_rank tribe_rank
    species_rank subspecies_rank variety_rank subvariety_rank form_rank subform_rank
    monomial binomial
    """.split()


# ####################################################################################
DELETE_MISSING_PARTS = "plant_missing_parts_v1"


@registry.misc(DELETE_MISSING_PARTS)
def delete_missing_parts(ent):
    """Remove trait if it is missing both the part and subpart."""
    data = ent._.data
    has_part = set(data.keys()) & plants.pylib.trait_lists.PARTS_SET
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
DELETE_WHEN = {
    "count": [DELETE_MISSING_PARTS, DELETE_PAGE_NO],
    "count_group": DELETE_MISSING_PARTS,
    "count_suffix": DELETE_MISSING_COUNT,
    "size": [DELETE_MISSING_PARTS, DELETE_KM],
}
