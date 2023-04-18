import re
from pathlib import Path

from spacy import registry
from traiter.traits import trait_util

from plants.traits import misc

PART_MATCH = "part_match"

PART_CSV = Path(__file__).parent / "part_terms.csv"
MISSING_CSV = Path(misc.__file__).parent / "missing_terms.csv"
ALL_CSVS = [PART_CSV, MISSING_CSV]

REPLACE = trait_util.term_data(ALL_CSVS, "replace")

NOT_PART = ["part_and", "part_leader", "part_missing", "subpart"]
PART_LABELS = [lb for lb in trait_util.get_labels(PART_CSV) if lb not in NOT_PART]

OTHER_LABELS = "missing_part missing_subpart multiple_parts subpart".split()
ALL_LABELS = PART_LABELS + OTHER_LABELS


@registry.misc(PART_MATCH)
def part_match(ent):
    frags = [[]]
    label = ent.label_
    relabel = ent.label_

    for token in ent:
        token._.flag = "part" if token._.term in PART_LABELS else "subpart"

        if relabel not in OTHER_LABELS and token._.term in PART_LABELS:
            relabel = token._.term

        if token._.term in ALL_LABELS:
            part = REPLACE.get(token.lower_, token.lower_)

            if part not in frags[-1]:
                frags[-1].append(part)

            if label not in ("missing_part", "multiple_parts", "subpart"):
                label = token._.term

        elif token._.term == "missing":
            frags[-1].append(REPLACE.get(token.lower_, token.lower_))

        elif token._.term == "part_and":
            frags.append([])

    all_parts = [" ".join(f) for f in frags]
    all_parts = [re.sub(r" - ", "-", p) for p in all_parts]
    all_parts = [REPLACE.get(p, p) for p in all_parts]

    ent._.relabel = relabel
    ent._.data["trait"] = relabel
    ent._.data[relabel] = all_parts[0] if len(all_parts) == 1 else all_parts

    ent[0]._.data = ent._.data  # Cache so we can use this in counts
