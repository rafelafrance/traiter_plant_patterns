from pathlib import Path

from spacy import Language
from traiter.pylib.traits import add_pipe as add
from traiter.pylib.traits import trait_util

from plants.pylib.traits.basic.custom_pipe import CUSTOM_PIPE

HERE = Path(__file__).parent
TRAIT = HERE.stem

CSV = HERE / f"{TRAIT}.csv"
SEX_CSV = HERE / "sex.csv"
ALL_CSVS = [CSV, SEX_CSV]

REMOVE = ["skip"]


def build(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name=f"{TRAIT}_terms", path=ALL_CSVS, **kwargs)

    config = {
        "replace": trait_util.term_data(ALL_CSVS, "replace"),
        "labels": trait_util.get_labels(ALL_CSVS),
    }
    prev = add.custom_pipe(nlp, CUSTOM_PIPE, config=config, after=prev)

    prev = add.cleanup_pipe(nlp, name=f"{TRAIT}_cleanup", remove=REMOVE, after=prev)

    return prev
