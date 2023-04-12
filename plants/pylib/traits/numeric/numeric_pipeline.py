from spacy import Language
from traiter.pylib.traits import add_pipe as add
from traiter.pylib.traits import trait_util

from .count_patterns import count_patterns
from .range_action import ALL_CSVS
from .range_patterns import range_patterns
from .size_patterns import size_patterns


def build(nlp: Language, **kwargs):

    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="numeric_terms", path=ALL_CSVS, **kwargs)

    prev = add.trait_pipe(
        nlp,
        name="range_patterns",
        compiler=range_patterns(),
        keep=["per_count"],
        after=prev,
    )

    prev = add.trait_pipe(
        nlp,
        name="numeric_patterns",
        compiler=count_patterns() + size_patterns(),
        after=prev,
    )

    remove = trait_util.labels_to_remove(ALL_CSVS, keep=["count", "size", "sex"])
    remove += """ not_numeric not_a_range not_a_count not_a_size range """.split()
    prev = add.cleanup_pipe(nlp, name="numeric_cleanup", remove=remove, after=prev)

    # prev = add.debug_tokens(nlp, after=prev)  # ################################

    return prev
