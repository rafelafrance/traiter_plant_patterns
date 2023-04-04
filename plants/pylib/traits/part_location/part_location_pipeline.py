from pathlib import Path

from spacy import Language
from traiter.pylib.traits import add_pipe as add
from traiter.pylib.traits import trait_util

from .part_location_custom_pipe import PART_LOCATION_CUSTOM_PIPE
from .part_location_pattern_compilers import LOCATION_ENTS
from .part_location_pattern_compilers import part_location_compilers


def build(nlp: Language, **kwargs):
    part_location_csv = Path(__file__).parent / "part_location_terms.csv"

    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(
            nlp, name="part_location_terms", path=part_location_csv, **kwargs
        )

    prev = add.ruler_pipe(
        nlp,
        name="part_location_patterns",
        compiler=part_location_compilers(),
        overwrite_ents=True,
        after=prev,
    )

    config = {
        "replace": trait_util.term_data(part_location_csv, "replace"),
        "labels": LOCATION_ENTS,
    }
    prev = add.custom_pipe(nlp, PART_LOCATION_CUSTOM_PIPE, config=config, after=prev)

    prev = add.cleanup_pipe(
        nlp,
        name="part_location_cleanup",
        remove=trait_util.labels_to_remove(part_location_csv, keep=LOCATION_ENTS),
        after=prev,
    )

    return prev
