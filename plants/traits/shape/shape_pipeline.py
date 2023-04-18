from spacy import Language
from traiter.traits import add_pipe as add
from traiter.traits import trait_util

from .shape_action import SHAPE_CSV
from .shape_patterns import shape_patterns


def build(nlp: Language, **kwargs):

    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="shape_terms", path=SHAPE_CSV, **kwargs)

    prev = add.trait_pipe(
        nlp,
        name="shape_patterns",
        compiler=shape_patterns(),
        after=prev,
    )

    prev = add.cleanup_pipe(
        nlp,
        name="shape_cleanup",
        remove=trait_util.labels_to_remove(SHAPE_CSV, keep="shape"),
        after=prev,
    )

    return prev
