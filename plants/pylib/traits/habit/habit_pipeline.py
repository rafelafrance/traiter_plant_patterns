from pathlib import Path

from spacy import Language
from traiter.pylib.traits import add_pipe as add
from traiter.pylib.traits import trait_util

from .habit_custom_pipe import HABIT_CUSTOM_PIPE
from .habit_pattern_compilers import HABIT_COMPILERS

HERE = Path(__file__).parent

CSV = HERE / "habit_terms.csv"
SHAPE_CSV = HERE.parent / "shape" / "shape_terms.csv"
ALL_CSVS = [CSV, SHAPE_CSV]


def build(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="habit_terms", path=ALL_CSVS, **kwargs)

    prev = add.ruler_pipe(
        nlp,
        name="habit_patterns",
        compiler=HABIT_COMPILERS,
        overwrite_ents=True,
        after=prev,
    )

    config = {
        "replace": trait_util.term_data(ALL_CSVS, "replace"),
    }
    prev = add.custom_pipe(nlp, HABIT_CUSTOM_PIPE, config=config, after=prev)

    prev = add.cleanup_pipe(
        nlp,
        name="habit_cleanup",
        remove=trait_util.labels_to_remove(CSV, keep="habit"),
        after=prev,
    )

    return prev
