from spacy import Language
from traiter.pylib import const as t_const
from traiter.pylib.traits import add_pipe as add

from . import link_taxon_like_patterns as pat


def build(nlp: Language, **kwargs):
    prev = add.link_pipe(
        nlp,
        name="link_taxon_like_patterns",
        compiler=pat.link_taxon_like_patterns(),
        parents=pat.TAXON_LIKE_PARENTS,
        children=pat.TAXON_LIKE_CHILDREN,
        weights=t_const.TOKEN_WEIGHTS,
        **kwargs,
    )

    return prev
