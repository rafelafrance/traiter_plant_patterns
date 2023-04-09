import os
from pathlib import Path

from spacy import Language
from traiter.pylib import taxon_util
from traiter.pylib.traits import add_pipe as add
from traiter.pylib.traits import trait_util

from .taxon_auth_action import TAXON_AUTH_CUSTOM_PIPE
from .taxon_auth_patterns import taxon_auth_compilers
from .taxon_auth_patterns import taxon_linnaeus_compilers
from .taxon_custom_pipe import TAXON_CUSTOM_PIPE
from .taxon_linnaeus_action import TAXON_LINNAEUS_CUSTOM_PIPE
from .taxon_patterns import taxon_compilers


def build(nlp: Language, authorities=2, **kwargs):
    terms = get_csvs()
    default_labels = {
        "binomial_terms": "binomial",
        "monomial_terms": "monomial",
        "mock_binomial_terms": "binomial",
        "mock_monomial_terms": "monomial",
    }

    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(
            nlp,
            name="taxon_terms",
            path=list(terms.values()),
            default_labels=default_labels,
            **kwargs,
        )

    prev = add.ruler_pipe(
        nlp,
        name="taxon_patterns",
        compiler=taxon_compilers(),
        overwrite_ents=True,
        after=prev,
    )

    config = {
        "level": trait_util.term_data(terms["rank_terms"], "level"),
        "rank_replace": trait_util.term_data(terms["rank_terms"], "replace"),
        "rank_abbrev": trait_util.term_data(terms["rank_terms"], "abbrev"),
        "monomial_ranks": trait_util.term_data(terms["monomial_terms"], "ranks"),
        "binomial_abbrev": taxon_util.abbrev_binomial_term(terms["binomial_terms"]),
    }
    prev = add.custom_pipe(nlp, TAXON_CUSTOM_PIPE, config=config, after=prev)
    # prev = add.merge_selected_ents(nlp, name="merge_taxon", labels="taxon", after=prev)

    prev = add.ruler_pipe(
        nlp,
        name="taxon_linnaeus_patterns",
        compiler=taxon_linnaeus_compilers(),
        overwrite_ents=True,
        after=prev,
    )

    prev = add.custom_pipe(nlp, TAXON_LINNAEUS_CUSTOM_PIPE, after=prev)

    # prev = add.debug_tokens(nlp, after=prev)  # #################################
    # prev = add.debug_ents(nlp, after=prev)  # #################################

    prev = add.ruler_pipe(
        nlp,
        name="taxon_auth_patterns",
        compiler=taxon_auth_compilers(),
        overwrite_ents=True,
        after=prev,
    )
    prev = add.debug_ents(nlp, after=prev)  # #################################
    prev = add.custom_pipe(nlp, TAXON_AUTH_CUSTOM_PIPE, after=prev)

    remove = trait_util.labels_to_remove(list(terms.values()), keep=["taxon"])
    remove += ["bad_taxon"]
    # prev = add.cleanup_pipe(nlp, name="taxon_cleanup", remove=remove, after=prev)

    return prev


def get_csvs():
    here = Path(__file__).parent
    terms = {
        "taxon_terms": here / "taxon_terms.csv",
        "rank_terms": here / "rank_terms.csv",
        "binomial_terms": here / "binomial_terms.zip",
        "monomial_terms": here / "monomial_terms.zip",
    }

    try:
        use_mock_taxa = int(os.getenv("MOCK_TAXA"))
    except (TypeError, ValueError):
        use_mock_taxa = 0

    if (
        not terms["binomial_terms"].exists()
        or not terms["monomial_terms"].exists()
        or use_mock_taxa
    ):
        terms["binomial_terms"] = here / "mock_binomial_terms.csv"
        terms["monomial_terms"] = here / "mock_monomial_terms.csv"

    return terms
