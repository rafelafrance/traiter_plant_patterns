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
from .numeric_pattern_compilers_count import count_compilers
from .numeric_pattern_compilers_range import range_compilers
from .numeric_pattern_compilers_size import size_compilers

HERE = Path(__file__).parent


def get_csvs():
    return [
        HERE / "numeric_terms.csv",
        Path(units.__file__).parent / "unit_distance_terms.csv",
        Path(units.__file__).parent / "unit_length_terms.csv",
        Path(units.__file__).parent / "unit_mass_terms.csv",
        HERE.parent / "basic" / "basic_missing_terms.csv",
        Path(month.__file__).parent / "month_terms.csv",
        Path(t_numeric.__file__).parent / "numeric_terms.csv",
        HERE.parent / "basic" / "basic_sex_terms.csv",
    ]


def build(nlp: Language, **kwargs):
    all_csvs = get_csvs()

    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name="numeric_terms", path=all_csvs, **kwargs)

    prev = add.ruler_pipe(
        nlp,
        name="range_patterns",
        compiler=range_compilers(),
        overwrite_ents=False,
        after=prev,
    )

    prev = add.custom_pipe(nlp, CUSTOM_PIPE_RANGE, after=prev)

    prev = add.ruler_pipe(
        nlp,
        name="numeric_patterns",
        compiler=count_compilers() + size_compilers(),
        overwrite_ents=True,
        after=prev,
    )

    replace = trait_util.term_data(all_csvs, "replace")

    config = {
        "replace": replace,
        "suffix_term": trait_util.term_data(all_csvs, "suffix_term"),
    }
    prev = add.custom_pipe(nlp, CUSTOM_PIPE_COUNT, config=config, after=prev)

    # prev = add.debug_tokens(nlp, after=prev)  # ################################

    config = {
        "replace": replace,
        "factors_cm": trait_util.term_data(all_csvs, "factor_cm", float),
    }
    prev = add.custom_pipe(nlp, CUSTOM_PIPE_SIZE, config=config, after=prev)

    remove = trait_util.labels_to_remove(all_csvs, keep=["count", "size", "sex"])
    remove += ["not_a_range", "not_a_count", "not_a_size"]
    prev = add.cleanup_pipe(nlp, name="numeric_cleanup", remove=remove, after=prev)

    return prev
