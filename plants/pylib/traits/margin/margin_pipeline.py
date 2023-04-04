from pathlib import Path

from spacy import Language
from traiter.pylib.traits import add_pipe as add
from traiter.pylib.traits import trait_util

from .margin_custom_pipe import MARGIN_CUSTOM_PIPE
from .margin_pattern_compilers import MARGIN_COMPILERS

HERE = Path(__file__).parent

CSV = HERE / "margin_terms.csv"


def build(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="margin_terms", path=CSV, **kwargs)

    prev = add.ruler_pipe(
        nlp,
        name="margin_patterns",
        compiler=MARGIN_COMPILERS,
        overwrite_ents=True,
        after=prev,
    )

    config = {"replace": trait_util.term_data(CSV, "replace")}
    prev = add.custom_pipe(nlp, MARGIN_CUSTOM_PIPE, config=config, after=prev)

    prev = add.cleanup_pipe(
        nlp,
        name="margin_cleanup",
        remove=trait_util.labels_to_remove(CSV, keep="margin"),
        after=prev,
    )

    return prev
