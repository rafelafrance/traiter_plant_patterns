from spacy import Language
from traiter.pylib.traits import add_pipe as add
from traiter.pylib.traits import trait_util

from . import shape_action as act
from . import shape_patterns as pat


def build(nlp: Language, **kwargs):

    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="shape_terms", path=act.SHAPE_CSV, **kwargs)

    prev = add.trait_pipe(
        nlp,
        name="shape_patterns",
        compiler=pat.shape_patterns(),
        after=prev,
    )

    prev = add.cleanup_pipe(
        nlp,
        name="shape_cleanup",
        remove=trait_util.labels_to_remove(act.SHAPE_CSV, keep="shape"),
        after=prev,
    )

    return prev
