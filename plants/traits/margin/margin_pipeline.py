from pathlib import Path

from spacy import Language
from traiter.traits import add_pipe as add
from traiter.traits import trait_util

from . import margin_patterns as pat


def build(nlp: Language, **kwargs):
    margin_csv = Path(__file__).parent / "margin_terms.csv"

    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="margin_terms", path=margin_csv, **kwargs)

    prev = add.trait_pipe(
        nlp,
        name="margin_patterns",
        compiler=pat.margin_patterns(),
        after=prev,
    )

    prev = add.cleanup_pipe(
        nlp,
        name="margin_cleanup",
        remove=trait_util.labels_to_remove(margin_csv, keep="margin"),
        after=prev,
    )

    return prev
