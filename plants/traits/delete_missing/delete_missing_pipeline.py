from spacy import Language
from traiter.traits import add_pipe as add

from .delete_missing_action import DELETE_MISSING
from plants.traits.part.part_patterns import PART_LABELS


def build(nlp: Language, **kwargs):
    config = {
        "check": ["count", "size"],
        "missing": PART_LABELS + ["subpart"],
    }
    prev = add.custom_pipe(nlp, DELETE_MISSING, config=config, **kwargs)

    return prev
