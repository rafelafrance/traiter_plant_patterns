from pathlib import Path

from spacy import Language
from traiter.pylib.traits import add_pipe as add
from traiter.pylib.traits import month
from traiter.pylib.traits import numeric as t_numeric
from traiter.pylib.traits import trait_util
from traiter.pylib.traits import units

from .numeric_custom_pipe_count import CUSTOM_PIPE_COUNT
from .numeric_custom_pipe_range import CUSTOM_PIPE_RANGE
from .numeric_custom_pipe_size import CUSTOM_PIPE_SIZE
from .numeric_pattern_compilers_count import COUNT_COMPILERS
from .numeric_pattern_compilers_range import RANGE_COMPILERS
from .numeric_pattern_compilers_size import SIZE_COMPILERS

HERE = Path(__file__).parent

CSV = HERE / "numeric_terms.csv"
DIST_CSV = Path(units.__file__).parent / "unit_distance_terms.csv"
LENGTH_CSV = Path(units.__file__).parent / "unit_length_terms.csv"
MASS_CSV = Path(units.__file__).parent / "unit_mass_terms.csv"
MISSING_CSV = HERE.parent / "basic" / "basic_missing_terms.csv"
MONTH_CSV = Path(month.__file__).parent / "month_terms.csv"
NUMERIC_CSV = Path(t_numeric.__file__).parent / "numeric_terms.csv"
SEX_CSV = HERE.parent / "basic" / "basic_sex_terms.csv"
ALL_CSVS = [
    CSV,
    MONTH_CSV,
    NUMERIC_CSV,
    SEX_CSV,
    LENGTH_CSV,
    MASS_CSV,
    DIST_CSV,
    MISSING_CSV,
]


def build(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="numeric_terms", path=ALL_CSVS, **kwargs)

    prev = add.ruler_pipe(
        nlp,
        name="range_patterns",
        compiler=RANGE_COMPILERS,
        overwrite_ents=False,
        after=prev,
    )

    prev = add.custom_pipe(nlp, CUSTOM_PIPE_RANGE, after=prev)

    prev = add.ruler_pipe(
        nlp,
        name="numeric_patterns",
        compiler=COUNT_COMPILERS + SIZE_COMPILERS,
        overwrite_ents=True,
        after=prev,
    )

    replace = trait_util.term_data(ALL_CSVS, "replace")

    config = {
        "replace": replace,
        "suffix_term": trait_util.term_data(CSV, "suffix_term"),
    }
    prev = add.custom_pipe(nlp, CUSTOM_PIPE_COUNT, config=config, after=prev)

    prev = add.debug_tokens(nlp, after=prev)  # ################################

    config = {
        "replace": replace,
        "factors_cm": trait_util.term_data(LENGTH_CSV, "factor_cm", float),
    }
    prev = add.custom_pipe(nlp, CUSTOM_PIPE_SIZE, config=config, after=prev)

    remove = trait_util.labels_to_remove(ALL_CSVS, keep=["count", "size", "sex"])
    remove += ["not_a_range", "not_a_count", "not_a_size"]
    prev = add.cleanup_pipe(nlp, name="numeric_cleanup", remove=remove, after=prev)

    return prev
