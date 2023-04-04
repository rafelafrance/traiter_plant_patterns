from pathlib import Path

from spacy import Language
from traiter.pylib.traits import add_pipe as add
from traiter.pylib.traits import trait_util

from .surface_custom_pipe import SURFACE_CUSTOM_PIPE
from .surface_pattern_compilers import surface_compilers


def build(nlp: Language, **kwargs):
    surface_csv = Path(__file__).parent / "surface_terms.csv"

    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="surface_terms", path=surface_csv, **kwargs)

    prev = add.ruler_pipe(
        nlp,
        name="surface_patterns",
        compiler=surface_compilers(),
        overwrite_ents=True,
        after=prev,
    )

    config = {"replace": trait_util.term_data(surface_csv, "replace")}
    prev = add.custom_pipe(nlp, SURFACE_CUSTOM_PIPE, config=config, after=prev)

    prev = add.cleanup_pipe(
        nlp,
        name="surface_cleanup",
        remove=trait_util.labels_to_remove(surface_csv, keep="surface"),
        after=prev,
    )

    return prev
