from pathlib import Path

from spacy import Language
from traiter.pylib.traits import add_pipe as add
from traiter.pylib.traits import trait_util

from .shape_custom_pipe import SHAPE_CUSTOM_PIPE
from .shape_pattern_compilers import shape_compilers


def build(nlp: Language, **kwargs):
    shape_csv = Path(__file__).parent / "shape_terms.csv"

    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="shape_terms", path=shape_csv, **kwargs)

    prev = add.ruler_pipe(
        nlp,
        name="shape_patterns",
        compiler=shape_compilers(),
        overwrite_ents=True,
        after=prev,
    )

    config = {"replace": trait_util.term_data(shape_csv, "replace")}
    prev = add.custom_pipe(nlp, SHAPE_CUSTOM_PIPE, config=config, after=prev)

    prev = add.cleanup_pipe(
        nlp,
        name="shape_cleanup",
        remove=trait_util.labels_to_remove(shape_csv, keep="shape"),
        after=prev,
    )

    return prev
