from spacy import Language
from traiter.pylib.traits import add_pipe as add

from ..part.part_patterns import PART_LABELS
from .delete_missing_action import DELETE_MISSING


def build(nlp: Language, **kwargs):
    config = {
        "check": ["count", "size"],
        "missing": PART_LABELS + ["subpart"],
    }
    prev = add.custom_pipe(nlp, DELETE_MISSING, config=config, **kwargs)

    return prev