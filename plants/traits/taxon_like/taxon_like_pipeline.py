from spacy import Language
from traiter.traits import add_pipe as add
from traiter.traits import trait_util

from .taxon_like_action import TAXON_LIKE_CSV
from .taxon_like_patterns import taxon_like_patterns


def build(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(
            nlp, name="taxon_like_terms", path=TAXON_LIKE_CSV, **kwargs
        )

    prev = add.trait_pipe(
        nlp,
        name="taxon_like_patterns",
        compiler=taxon_like_patterns(),
        after=prev,
    )

    prev = add.cleanup_pipe(
        nlp,
        name="taxon_like_cleanup",
        remove=trait_util.labels_to_remove(TAXON_LIKE_CSV, keep="taxon_like"),
        after=prev,
    )

    return prev
