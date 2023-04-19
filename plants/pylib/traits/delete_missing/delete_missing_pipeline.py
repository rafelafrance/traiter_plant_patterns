from spacy import Language
from traiter.pylib.traits import add_pipe as add

from . import delete_missing_action as act
from plants.pylib.traits.part import part_action as p_act


def build(nlp: Language, **kwargs):
    config = {
        "check": ["count", "size"],
        "missing": p_act.PART_LABELS + ["subpart"],
    }
    prev = add.custom_pipe(nlp, act.DELETE_MISSING, config=config, **kwargs)

    return prev
