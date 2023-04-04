from pathlib import Path

from spacy import Language
from traiter.pylib.traits import add_pipe as add
from traiter.pylib.traits import trait_util

from .surface_custom_pipe import SURFACE_CUSTOM_PIPE
from .surface_pattern_compilers import SURFACE_COMPILERS

CSV = Path(__file__).parent / "surface_terms.csv"


def build(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="surface_terms", path=CSV, **kwargs)

    prev = add.ruler_pipe(
        nlp,
        name="surface_patterns",
        compiler=SURFACE_COMPILERS,
        after=prev,
        overwrite_ents=True,
    )

    config = {"replace": trait_util.term_data(CSV, "replace")}
    prev = add.custom_pipe(nlp, SURFACE_CUSTOM_PIPE, config=config, after=prev)

    prev = add.cleanup_pipe(
        nlp,
        name="surface_cleanup",
        remove=trait_util.labels_to_remove(CSV, keep="surface"),
        after=prev,
    )

    return prev
