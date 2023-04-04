from pathlib import Path

from spacy import Language
from traiter.pylib.traits import add_pipe as add
from traiter.pylib.traits import trait_util

from plants.pylib.traits.basic.basic_custom_pipe import BASIC_CUSTOM_PIPE


def get_csvs():
    here = Path(__file__).parent
    return [
        here / "basic_terms.csv",
        here / "basic_sex_terms.csv",
        here / "basic_missing_terms.csv",
    ]


def build(nlp: Language, **kwargs):
    all_csvs = get_csvs()

    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="basic_terms", path=all_csvs, **kwargs)

    config = {
        "replace": trait_util.term_data(all_csvs, "replace"),
        "labels": trait_util.get_labels(all_csvs),
    }
    prev = add.custom_pipe(nlp, BASIC_CUSTOM_PIPE, config=config, after=prev)

    return prev
