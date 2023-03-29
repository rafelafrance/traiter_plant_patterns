"""Link traits to plant parts.

We are linking parts like "petal" or "leaf" to traits like color or size.
For example: "with thick, woody rootstock" should link the "rootstock" part with
the "woody" trait.
"""
from pathlib import Path

from spacy import Language
from traiter.pylib import add_pipe as add
from traiter.pylib import const as t_const
from traiter.pylib import trait_util

from . import link_part_compilers as comp

HERE = Path(__file__).parent


def pipe(nlp: Language, **kwargs):
    patterns = trait_util.get_patterns(HERE / "link_part_patterns.jsonl")
    prev = add.link_pipe(
        nlp,
        patterns,
        name="link_part",
        parents=comp.PART_PARENTS,
        children=comp.PART_CHILDREN,
        weights=t_const.TOKEN_WEIGHTS,
        reverse_weights=t_const.REVERSE_WEIGHTS,
        **kwargs,
    )

    patterns = trait_util.get_patterns(HERE / "link_part_once_patterns.jsonl")
    prev = add.link_pipe(
        nlp,
        patterns,
        name="link_part_once",
        parents=comp.PART_PARENTS,
        children=comp.PART_ONCE_CHILDREN,
        weights=t_const.TOKEN_WEIGHTS,
        max_links=1,
        differ=["sex", "dimensions"],
        after=prev,
    )

    patterns = trait_util.get_patterns(HERE / "link_subpart_patterns.jsonl")
    prev = add.link_pipe(
        nlp,
        patterns,
        name="link_subpart",
        parents=comp.SUBPART_PARENTS,
        children=comp.SUBPART_CHILDREN,
        weights=t_const.TOKEN_WEIGHTS,
        after=prev,
    )

    return prev
