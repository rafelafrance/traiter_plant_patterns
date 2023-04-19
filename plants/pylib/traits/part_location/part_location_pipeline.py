from spacy import Language
from traiter.pylib.traits import add_pipe as add
from traiter.pylib.traits import trait_util

from . import part_location_action as act
from . import part_location_patterns as pat


def build(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(
            nlp, name="part_location_terms", path=act.ALL_CSVS, **kwargs
        )

    prev = add.trait_pipe(
        nlp,
        name="part_location_patterns",
        compiler=pat.part_location_patterns(),
        after=prev,
    )

    prev = add.cleanup_pipe(
        nlp,
        name="part_location_cleanup",
        remove=trait_util.labels_to_remove(act.ALL_CSVS, keep=pat.LOCATION_ENTS),
        after=prev,
    )

    return prev
