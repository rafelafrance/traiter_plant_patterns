from spacy import Language
from traiter.pylib.traits import add_pipe as add

from . import taxon_like_action as act
from . import taxon_like_patterns as pat


def build(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(
            nlp, name="taxon_like_terms", path=act.TAXON_LIKE_CSV, **kwargs
        )

    prev = add.trait_pipe(
        nlp,
        name="taxon_like_patterns",
        compiler=pat.taxon_like_patterns(),
        after=prev,
    )

    prev = add.cleanup_pipe(nlp, name="taxon_like_cleanup", after=prev)

    return prev
