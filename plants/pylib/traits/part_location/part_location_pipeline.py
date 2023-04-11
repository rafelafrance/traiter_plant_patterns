from spacy import Language
from traiter.pylib.traits import add_pipe as add
from traiter.pylib.traits import trait_util

from .part_location_action import ALL_CSVS
from .part_location_patterns import LOCATION_ENTS
from .part_location_patterns import part_location_patterns


def build(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="part_location_terms", path=ALL_CSVS, **kwargs)

    prev = add.trait_pipe(
        nlp,
        name="part_location_patterns",
        compiler=part_location_patterns(),
        after=prev,
    )

    prev = add.cleanup_pipe(
        nlp,
        name="part_location_cleanup",
        remove=trait_util.labels_to_remove(ALL_CSVS, keep=LOCATION_ENTS),
        after=prev,
    )

    return prev
