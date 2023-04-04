from pathlib import Path

from spacy import Language
from traiter.pylib.traits import add_pipe as add
from traiter.pylib.traits import trait_util

from .part_custom_pipe import PART_CUSTOM_PIPE
from .part_pattern_compilers import PART_COMPILERS
from .part_pattern_compilers import PART_LABELS

HERE = Path(__file__).parent
TRAIT = HERE.stem

CSV = HERE / "part_terms.csv"
MISSING_CSV = HERE.parent / "basic" / "basic_missing_terms.csv"
ALL_CSVS = [CSV, MISSING_CSV]

ALL_LABELS = PART_LABELS + "missing_part missing_subpart multiple_parts subpart".split()


def build(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(
            nlp, name="part_terms", path=ALL_CSVS, overwrite_ents=True, **kwargs
        )

    prev = add.ruler_pipe(
        nlp,
        name="part_patterns",
        compiler=PART_COMPILERS,
        overwrite_ents=True,
        after=prev,
    )

    config = {
        "replace": trait_util.term_data(CSV, "replace"),
        "labels": ALL_LABELS,
    }
    prev = add.custom_pipe(nlp, PART_CUSTOM_PIPE, config=config, after=prev)

    prev = add.cleanup_pipe(
        nlp,
        name="part_cleanup",
        remove=trait_util.labels_to_remove(ALL_CSVS, keep=ALL_LABELS) + ["not_a_part"],
        after=prev,
    )

    return prev
