from pathlib import Path

from spacy import Language
from traiter.pylib.traits import add_pipe as add
from traiter.pylib.traits import trait_util

from .habit_custom_pipe import HABIT_CUSTOM_PIPE
from .habit_pattern_compilers import habit_compilers


def get_csvs():
    here = Path(__file__).parent
    return [
        here / "habit_terms.csv",
        here.parent / "shape" / "shape_terms.csv",
    ]


def build(nlp: Language, **kwargs):
    all_csvs = get_csvs()

    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="habit_terms", path=all_csvs, **kwargs)

    prev = add.ruler_pipe(
        nlp,
        name="habit_patterns",
        compiler=habit_compilers(),
        overwrite_ents=True,
        after=prev,
    )

    config = {
        "replace": trait_util.term_data(all_csvs, "replace"),
    }
    prev = add.custom_pipe(nlp, HABIT_CUSTOM_PIPE, config=config, after=prev)

    prev = add.cleanup_pipe(
        nlp,
        name="habit_cleanup",
        remove=trait_util.labels_to_remove(all_csvs, keep="habit"),
        after=prev,
    )

    return prev
