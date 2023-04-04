from pathlib import Path

from spacy import Language
from traiter.pylib.traits import add_pipe as add
from traiter.pylib.traits import trait_util

from .margin_custom_pipe import MARGIN_CUSTOM_PIPE
from .margin_pattern_compilers import margin_compilers


def build(nlp: Language, **kwargs):
    margin_csv = Path(__file__).parent / "margin_terms.csv"

    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="margin_terms", path=margin_csv, **kwargs)

    prev = add.ruler_pipe(
        nlp,
        name="margin_patterns",
        compiler=margin_compilers(),
        overwrite_ents=True,
        after=prev,
    )

    config = {"replace": trait_util.term_data(margin_csv, "replace")}
    prev = add.custom_pipe(nlp, MARGIN_CUSTOM_PIPE, config=config, after=prev)

    prev = add.cleanup_pipe(
        nlp,
        name="margin_cleanup",
        remove=trait_util.labels_to_remove(margin_csv, keep="margin"),
        after=prev,
    )

    return prev
