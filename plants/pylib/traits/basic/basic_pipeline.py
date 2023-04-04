from pathlib import Path

from spacy import Language
from traiter.pylib.traits import add_pipe as add
from traiter.pylib.traits import trait_util

from plants.pylib.traits.basic.basic_custom_pipe import BASIC_CUSTOM_PIPE

HERE = Path(__file__).parent
TRAIT = HERE.stem

CSV = HERE / "basic_terms.csv"
SEX_CSV = HERE / "basic_sex_terms.csv"
MISSING_CSV = HERE / "basic_missing_terms.csv"
ALL_CSVS = [CSV, MISSING_CSV, SEX_CSV]


def build(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="basic_terms", path=ALL_CSVS, **kwargs)

    config = {
        "replace": trait_util.term_data(ALL_CSVS, "replace"),
        "labels": trait_util.get_labels(ALL_CSVS),
    }
    prev = add.custom_pipe(nlp, BASIC_CUSTOM_PIPE, config=config, after=prev)

    return prev
