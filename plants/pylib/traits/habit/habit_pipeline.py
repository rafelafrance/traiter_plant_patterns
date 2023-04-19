from pathlib import Path

from spacy import Language
from traiter.pylib.traits import add_pipe as add
from traiter.pylib.traits import trait_util

from . import habit_patterns as pat


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

    prev = add.trait_pipe(
        nlp,
        name="habit_patterns",
        compiler=pat.habit_patterns(),
        after=prev,
    )

    prev = add.cleanup_pipe(
        nlp,
        name="habit_cleanup",
        remove=trait_util.labels_to_remove(all_csvs, keep="habit"),
        after=prev,
    )

    return prev
