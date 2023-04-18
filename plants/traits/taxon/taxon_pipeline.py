from spacy import Language
from traiter.traits import add_pipe as add
from traiter.traits import trait_util

from .taxon_action import ALL_CSVS
from .taxon_action import TAXON_LABELS
from .taxon_action import TAXON_LABELS_PLUS
from .taxon_auth_patterns import taxon_auth_patterns
from .taxon_auth_patterns import taxon_linnaeus_patterns
from .taxon_extend_patterns import taxon_extend_patterns
from .taxon_patterns import multi_taxon_patterns
from .taxon_patterns import taxon_patterns
from .taxon_patterns import taxon_rename_patterns


def build(nlp: Language, extend=1, **kwargs):
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
            path=list(ALL_CSVS.values()),
            default_labels=default_labels,
            **kwargs,
        )

    prev = add.trait_pipe(
        nlp,
        name="taxon_patterns",
        compiler=taxon_patterns(),
        merge=TAXON_LABELS,
        after=prev,
    )

    prev = add.trait_pipe(
        nlp,
        name="taxon_linnaeus_patterns",
        compiler=taxon_linnaeus_patterns() + multi_taxon_patterns(),
        merge=TAXON_LABELS_PLUS,
        after=prev,
    )

    prev = add.trait_pipe(
        nlp,
        name="taxon_auth_patterns",
        compiler=taxon_auth_patterns(),
        merge=TAXON_LABELS_PLUS,
        keep=["singleton"],
        after=prev,
    )

    for i in range(1, extend + 1):
        name = f"taxon_extend_{i}"
        prev = add.trait_pipe(
            nlp,
            name=name,
            compiler=taxon_extend_patterns(),
            merge=TAXON_LABELS_PLUS,
            after=prev,
        )

    prev = add.trait_pipe(
        nlp,
        name="taxon_rename",
        compiler=taxon_rename_patterns(),
        after=prev,
    )

    # prev = add.debug_tokens(nlp, after=prev)  # #################################
    # prev = add.debug_ents(nlp, after=prev)  # ###################################

    csvs = [ALL_CSVS["taxon_terms"], ALL_CSVS["rank_terms"]]
    remove = trait_util.labels_to_remove(csvs, keep=["taxon"])
    remove += ["bad_taxon", "monomial", "binomial"]
    prev = add.cleanup_pipe(nlp, name="taxon_cleanup", remove=remove, after=prev)

    return prev
