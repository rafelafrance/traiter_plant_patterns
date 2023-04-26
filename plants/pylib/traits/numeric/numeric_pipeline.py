from spacy.language import Language
from traiter.pylib.traits import add_pipe as add
from traiter.pylib.traits import pattern_compiler

from . import count_patterns as c_pat
from . import range_action as act
from . import range_patterns as r_pat
from . import size_patterns as s_pat


def build(nlp: Language, **kwargs):

    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="numeric_terms", path=act.ALL_CSVS, **kwargs)

    prev = add.trait_pipe(
        nlp,
        name="range_patterns",
        compiler=r_pat.range_patterns(),
        keep=pattern_compiler.ACCUMULATOR.keep + ["per_count"],
        after=prev,
    )

    prev = add.trait_pipe(
        nlp,
        name="numeric_patterns",
        compiler=c_pat.count_patterns() + s_pat.size_patterns(),
        after=prev,
    )

    prev = add.cleanup_pipe(nlp, name="numeric_cleanup", after=prev)

    # prev = add.debug_tokens(nlp, after=prev)  # ################################

    return prev
