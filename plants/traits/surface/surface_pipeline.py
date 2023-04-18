from spacy import Language
from traiter.traits import add_pipe as add
from traiter.traits import trait_util

from .surface_action import SURFACE_CSV
from .surface_patterns import surface_patterns


def build(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="surface_terms", path=SURFACE_CSV, **kwargs)

    prev = add.trait_pipe(
        nlp,
        name="surface_patterns",
        compiler=surface_patterns(),
        after=prev,
    )

    prev = add.cleanup_pipe(
        nlp,
        name="surface_cleanup",
        remove=trait_util.labels_to_remove(SURFACE_CSV, keep="surface"),
        after=prev,
    )

    return prev
