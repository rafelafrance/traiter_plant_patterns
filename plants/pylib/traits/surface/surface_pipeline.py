from spacy import Language
from traiter.pylib.traits import add_pipe as add

from . import surface_action as act
from . import surface_patterns as pat


def build(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="surface_terms", path=act.SURFACE_CSV, **kwargs)

    prev = add.trait_pipe(
        nlp,
        name="surface_patterns",
        compiler=pat.surface_patterns(),
        after=prev,
    )

    prev = add.cleanup_pipe(nlp, name="surface_cleanup", after=prev)

    return prev
