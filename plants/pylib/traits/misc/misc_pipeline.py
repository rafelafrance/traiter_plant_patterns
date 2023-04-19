from spacy import Language
from traiter.pylib.traits import add_pipe as add

from . import misc_action as act
from . import misc_patterns as pat


def build(nlp: Language, **kwargs):

    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="misc_terms", path=act.ALL_CSVS, **kwargs)

    prev = add.trait_pipe(
        nlp,
        name="misc_patterns",
        compiler=pat.misc_patterns(),
        after=prev,
    )

    return prev
