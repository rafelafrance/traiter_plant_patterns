from pathlib import Path

from spacy import Language
from traiter.pylib.traits import add_pipe as add
from traiter.pylib.traits import trait_util

from .shape_custom_pipe import SHAPE_CUSTOM_PIPE
from .shape_pattern_compilers import SHAPE_COMPILERS

CSV = Path(__file__).parent / "shape_terms.csv"


def build(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="shape_terms", path=CSV, **kwargs)

    prev = add.ruler_pipe(
        nlp,
        name="shape_patterns",
        compiler=SHAPE_COMPILERS,
        overwrite_ents=True,
        after=prev,
    )

    config = {"replace": trait_util.term_data(CSV, "replace")}
    prev = add.custom_pipe(nlp, SHAPE_CUSTOM_PIPE, config=config, after=prev)

    prev = add.cleanup_pipe(
        nlp,
        name="shape_cleanup",
        remove=trait_util.labels_to_remove(CSV, keep="shape"),
        after=prev,
    )

    return prev
