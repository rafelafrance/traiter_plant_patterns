from pathlib import Path

from spacy import Language
from traiter.pylib.traits import add_pipe as add
from traiter.pylib.traits import trait_util

from .part_custom_pipe import PART_CUSTOM_PIPE
from .part_pattern_compilers import part_compilers
from .part_pattern_compilers import PART_LABELS

ALL_LABELS = PART_LABELS + "missing_part missing_subpart multiple_parts subpart".split()


def get_csvs():
    here = Path(__file__).parent
    return [
        here / "part_terms.csv",
        here.parent / "misc" / "missing_terms.csv",
    ]


def build(nlp: Language, **kwargs):
    all_csvs = get_csvs()

    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(
            nlp, name="part_terms", path=all_csvs, overwrite_ents=True, **kwargs
        )

    prev = add.ruler_pipe(
        nlp,
        name="part_patterns",
        compiler=part_compilers(),
        overwrite_ents=True,
        after=prev,
    )

    config = {
        "replace": trait_util.term_data(all_csvs, "replace"),
        "labels": ALL_LABELS,
    }
    prev = add.custom_pipe(nlp, PART_CUSTOM_PIPE, config=config, after=prev)

    prev = add.cleanup_pipe(
        nlp,
        name="part_cleanup",
        remove=trait_util.labels_to_remove(all_csvs, keep=ALL_LABELS) + ["not_a_part"],
        after=prev,
    )

    return prev
