from spacy import Language
from traiter.pylib.traits import add_pipe as add
from traiter.pylib.traits import trait_util

from .part_action import ALL_CSVS
from .part_action import ALL_LABELS
from .part_patterns import part_patterns


def build(nlp: Language, **kwargs):

    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="part_terms", path=ALL_CSVS, **kwargs)

    # prev = add.debug_tokens(nlp, after=prev)  # ################################

    prev = add.trait_pipe(
        nlp,
        name="part_patterns",
        compiler=part_patterns(),
        after=prev,
    )

    prev = add.cleanup_pipe(
        nlp,
        name="part_cleanup",
        remove=trait_util.labels_to_remove(ALL_CSVS, keep=ALL_LABELS) + ["not_a_part"],
        after=prev,
    )

    return prev
