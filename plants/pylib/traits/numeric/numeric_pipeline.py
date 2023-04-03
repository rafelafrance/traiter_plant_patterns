from pathlib import Path

from spacy import Language
from traiter.pylib.traits import add_pipe as add
from traiter.pylib.traits import month
from traiter.pylib.traits import numeric as t_numeric
from traiter.pylib.traits import trait_util
from traiter.pylib.traits import units

from .custom_pipe_count import CUSTOM_PIPE_COUNT
from .custom_pipe_range import CUSTOM_PIPE_RANGE
from .custom_pipe_size import CUSTOM_PIPE_SIZE
from .pattern_compilers_count import COMPILERS as COUNT_COMPILERS
from .pattern_compilers_range import COMPILERS as RANGE_COMPILERS
from .pattern_compilers_size import COMPILERS as SIZE_COMPILERS

HERE = Path(__file__).parent
TRAIT = HERE.stem

CSV = HERE / f"{TRAIT}.csv"
MONTH_CSV = Path(month.__file__).parent / "month.csv"
NUMERIC_CSV = Path(t_numeric.__file__).parent / "numeric.csv"
SEX_CSV = HERE.parent / "basic" / "sex.csv"
LENGTH_CSV = Path(units.__file__).parent / "units_length.csv"
MASS_CSV = Path(units.__file__).parent / "units_mass.csv"
DIST_CSV = Path(units.__file__).parent / "units_distance.csv"
ALL_CSV = [CSV, MONTH_CSV, NUMERIC_CSV, SEX_CSV, LENGTH_CSV, MASS_CSV, DIST_CSV]


def build(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(
            nlp, name=f"{TRAIT}_terms", path=ALL_CSV, overwrite_ents=True, **kwargs
        )

    prev = add.ruler_pipe(
        nlp,
        name="range_patterns",
        compiler=RANGE_COMPILERS,
        overwrite_ents=False,
        after=prev,
    )

    config = {"trait": "range"}
    prev = add.custom_pipe(nlp, CUSTOM_PIPE_RANGE, config=config, after=prev)

    prev = add.ruler_pipe(
        nlp,
        name="numeric_patterns",
        compiler=COUNT_COMPILERS + SIZE_COMPILERS,
        overwrite_ents=True,
        after=prev,
    )

    # from traiter.pylib.pipes import debug  # #####################################
    # prev = debug.tokens(nlp, after=prev)  # ######################################

    replace = trait_util.term_data(ALL_CSV, "replace")

    config = {
        "trait": "count",
        "replace": replace,
        "suffix_term": trait_util.term_data(CSV, "suffix_term"),
    }
    prev = add.custom_pipe(nlp, CUSTOM_PIPE_COUNT, config=config, after=prev)

    config = {
        "trait": "size",
        "replace": replace,
        "factors_cm": trait_util.term_data(LENGTH_CSV, "factor_cm", float),
    }
    prev = add.custom_pipe(nlp, CUSTOM_PIPE_SIZE, config=config, after=prev)

    remove = trait_util.labels_to_remove(ALL_CSV, keep=["count", "size", "sex"])
    remove += ["not_a_range", "not_a_count", "not_a_size"]
    prev = add.cleanup_pipe(nlp, name=f"{TRAIT}_cleanup", remove=remove, after=prev)

    return prev
