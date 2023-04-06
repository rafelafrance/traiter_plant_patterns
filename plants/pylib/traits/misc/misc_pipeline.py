from pathlib import Path

from spacy import Language
from traiter.pylib.traits import add_pipe as add
from traiter.pylib.traits import trait_util

from plants.pylib.traits.misc.misc_custom_pipe import MISC_CUSTOM_PIPE


def get_csvs():
    here = Path(__file__).parent
    return [
        here / "misc_terms.csv",
        here / "missing_terms.csv",
        here / "sex_terms.csv",
    ]


def build(nlp: Language, **kwargs):
    all_csvs = get_csvs()

    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="misc_terms", path=all_csvs, **kwargs)

    config = {
        "replace": trait_util.term_data(all_csvs, "replace"),
        "labels": trait_util.get_labels(all_csvs),
    }
    prev = add.custom_pipe(nlp, MISC_CUSTOM_PIPE, config=config, after=prev)

    return prev
