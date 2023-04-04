"""Link traits to plant parts.

We are linking parts like "petal" or "leaf" to traits like color or size.
For example: "with thick, woody rootstock" should link the "rootstock" part with
the "woody" trait.
"""
from spacy import Language
from traiter.pylib import const as t_const
from traiter.pylib.traits import add_pipe as add

from . import link_part_pattern_compilers as comp


def build(nlp: Language, **kwargs):
    prev = add.link_pipe(
        nlp,
        name="link_part",
        compiler=comp.LINK_PART,
        parents=comp.LINK_PART_PARENTS,
        children=comp.LINK_PART_CHILDREN,
        weights=t_const.TOKEN_WEIGHTS,
        reverse_weights=t_const.REVERSE_WEIGHTS,
        **kwargs,
    )

    prev = add.link_pipe(
        nlp,
        name="link_part_once",
        compiler=comp.LINK_PART_ONCE,
        parents=comp.LINK_PART_PARENTS,
        children=comp.LINK_PART_ONCE_CHILDREN,
        weights=t_const.TOKEN_WEIGHTS,
        max_links=1,
        differ=["sex", "dimensions"],
        after=prev,
    )

    prev = add.link_pipe(
        nlp,
        name="link_subpart",
        compiler=comp.LINK_SUBPART,
        parents=comp.LINK_SUBPART_PARENTS,
        children=comp.LINK_SUBPART_CHILDREN,
        weights=t_const.TOKEN_WEIGHTS,
        after=prev,
    )

    prev = add.link_pipe(
        nlp,
        name="link_subpart_once",
        compiler=comp.LINK_SUBPART_ONCE,
        parents=comp.LINK_SUBPART_PARENTS,
        children=comp.LINK_PART_ONCE_CHILDREN,
        weights=t_const.TOKEN_WEIGHTS,
        max_links=1,
        differ=["sex", "dimensions"],
        after=prev,
    )

    return prev
