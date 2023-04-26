from spacy import Language
from traiter.pylib.traits import add_pipe as add
from traiter.pylib.traits import pattern_compiler as comp

from . import taxon_action as t_act
from . import taxon_auth_patterns as a_pat
from . import taxon_extend_patterns as e_pat
from . import taxon_patterns as t_pat


def build(nlp: Language, extend=1, **kwargs):
    keep = comp.ACCUMULATOR.keep  # Get them before we add to the list

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
            path=list(t_act.ALL_CSVS.values()),
            default_labels=default_labels,
            **kwargs,
        )

    prev = add.trait_pipe(
        nlp,
        name="taxon_patterns",
        compiler=t_pat.taxon_patterns(),
        keep=keep,
        merge=t_act.TAXON_LABELS,
        after=prev,
    )

    prev = add.trait_pipe(
        nlp,
        name="taxon_linnaeus_patterns",
        compiler=a_pat.taxon_linnaeus_patterns() + t_pat.multi_taxon_patterns(),
        keep=keep,
        merge=t_act.TAXON_LABELS_PLUS,
        after=prev,
    )

    prev = add.trait_pipe(
        nlp,
        name="taxon_auth_patterns",
        compiler=a_pat.taxon_auth_patterns(),
        merge=t_act.TAXON_LABELS_PLUS,
        keep=[*keep, "singleton"],
        after=prev,
    )

    for i in range(1, extend + 1):
        name = f"taxon_extend_{i}"
        prev = add.trait_pipe(
            nlp,
            name=name,
            compiler=e_pat.taxon_extend_patterns(),
            merge=t_act.TAXON_LABELS_PLUS,
            after=prev,
        )

    prev = add.trait_pipe(
        nlp,
        name="taxon_rename",
        compiler=t_pat.taxon_rename_patterns(),
        after=prev,
    )

    # prev = add.debug_tokens(nlp, after=prev)  # #################################
    # prev = add.debug_ents(nlp, after=prev)  # ###################################

    prev = add.cleanup_pipe(nlp, name="taxon_cleanup", after=prev)

    return prev
