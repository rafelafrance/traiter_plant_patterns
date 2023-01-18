import spacy
from traiter.patterns import matcher_patterns
from traiter.pipes.add_traits_pipe import ADD_TRAITS
from traiter.pipes.delete_traits_pipe import DELETE_TRAITS
from traiter.pipes.link_traits_pipe import LINK_TRAITS
from traiter.pipes.merge_traits import MERGE_TRAITS
from traiter.pipes.simple_traits_pipe import SIMPLE_TRAITS
from traiter.pipes.term_pipe import TERM_PIPE

from . import consts
from . import tokenizer
from .patterns import color_patterns
from .patterns import count_patterns
from .patterns import count_suffix_patterns
from .patterns import delete_patterns
from .patterns import habit_patterns
from .patterns import location_linker_patterns
from .patterns import margin_patterns
from .patterns import part_linker_patterns
from .patterns import part_location_patterns
from .patterns import part_patterns
from .patterns import range_patterns
from .patterns import sex_linker_patterns
from .patterns import shape_patterns
from .patterns import size_patterns
from .patterns import subpart_linker_patterns
from .patterns import subpart_patterns
from .patterns import taxon_like_linker_patterns
from .patterns import taxon_like_patterns
from .patterns import taxon_patterns
from .patterns import term_patterns

# from traiter.pipes import debug_pipes


def pipeline():
    nlp = spacy.load("en_core_web_sm", exclude=["ner"])

    tokenizer.setup_tokenizer(nlp)

    nlp.add_pipe(
        TERM_PIPE,
        before="parser",
        config={
            "terms": term_patterns.TERMS.terms,
            "replace": term_patterns.REPLACE,
        },
    )
    nlp.add_pipe("merge_entities", name="merge_terms")

    nlp.add_pipe(
        ADD_TRAITS,
        name="range_pipe",
        config={
            "patterns": matcher_patterns.as_dicts(
                [
                    range_patterns.RANGE_LOW,
                    range_patterns.RANGE_MIN_LOW,
                    range_patterns.RANGE_LOW_HIGH,
                    range_patterns.RANGE_LOW_MAX,
                    range_patterns.RANGE_MIN_LOW_HIGH,
                    range_patterns.RANGE_MIN_LOW_MAX,
                    range_patterns.RANGE_LOW_HIGH_MAX,
                    range_patterns.RANGE_MIN_LOW_HIGH_MAX,
                    range_patterns.NOT_A_RANGE,
                ]
            )
        },
    )
    nlp.add_pipe("merge_entities")

    nlp.add_pipe(
        ADD_TRAITS,
        name="part_traits",
        config={
            "patterns": matcher_patterns.as_dicts(
                [
                    part_patterns.PART,
                    part_patterns.MISSING_PART,
                    subpart_patterns.SUBPART,
                    subpart_patterns.SUBPART_SUFFIX,
                ]
            )
        },
    )

    nlp.add_pipe(
        SIMPLE_TRAITS,
        config={
            "replace": term_patterns.REPLACE,
            "exclude": ["multiple_parts", "subpart_suffix"],
        },
    )

    nlp.add_pipe(
        ADD_TRAITS,
        name="numeric_traits",
        config={
            "patterns": matcher_patterns.as_dicts(
                [
                    size_patterns.SIZE,
                    size_patterns.SIZE_HIGH_ONLY,
                    size_patterns.SIZE_DOUBLE_DIM,
                    size_patterns.NOT_A_SIZE,
                    part_location_patterns.PART_AS_DISTANCE,
                    count_patterns.COUNT,
                    count_patterns.COUNT_WORD,
                    count_patterns.NOT_A_COUNT,
                    count_suffix_patterns.COUNT_SUFFIX,
                    count_suffix_patterns.COUNT_SUFFIX_WORD,
                    taxon_patterns.TAXON,
                    taxon_patterns.MULTI_TAXON,
                ]
            )
        },
    )

    nlp.add_pipe(
        ADD_TRAITS,
        name="relative_traits",
        config={
            "patterns": matcher_patterns.as_dicts([taxon_like_patterns.TAXON_LIKE])
        },
    )

    nlp.add_pipe(
        ADD_TRAITS,
        name="group_traits",
        config={
            "patterns": matcher_patterns.as_dicts(
                [
                    color_patterns.COLOR,
                    margin_patterns.MARGIN,
                    shape_patterns.N_SHAPE,
                    shape_patterns.SHAPE,
                    part_location_patterns.PART_AS_LOCATION,
                    part_location_patterns.SUBPART_AS_LOCATION,
                    habit_patterns.HABIT,
                ]
            )
        },
    )

    nlp.add_pipe(DELETE_TRAITS, config={"delete": delete_patterns.PARTIAL_TRAITS})

    nlp.add_pipe(MERGE_TRAITS)

    nlp.add_pipe(
        LINK_TRAITS,
        name="link_parts",
        config={
            "parents": part_linker_patterns.PART_PARENTS,
            "children": part_linker_patterns.PART_CHILDREN,
            "weights": consts.TOKEN_WEIGHTS,
            "reverse_weights": consts.REVERSE_WEIGHTS,
            "patterns": matcher_patterns.as_dicts([part_linker_patterns.PART_LINKER]),
        },
    )

    nlp.add_pipe(
        LINK_TRAITS,
        name="link_parts_once",
        config={
            "parents": part_linker_patterns.LINK_PART_ONCE_PARENTS,
            "children": part_linker_patterns.LINK_PART_ONCE_CHILDREN,
            "weights": consts.TOKEN_WEIGHTS,
            "max_links": 1,
            "differ": ["sex", "dimensions"],
            "patterns": matcher_patterns.as_dicts(
                [part_linker_patterns.LINK_PART_ONCE]
            ),
        },
    )

    nlp.add_pipe(
        LINK_TRAITS,
        name="link_subparts",
        config={
            "parents": subpart_linker_patterns.SUBPART_PARENTS,
            "children": subpart_linker_patterns.SUBPART_CHILDREN,
            "weights": consts.TOKEN_WEIGHTS,
            "patterns": matcher_patterns.as_dicts(
                [subpart_linker_patterns.SUBPART_LINKER]
            ),
        },
    )

    nlp.add_pipe(
        LINK_TRAITS,
        name="link_subparts_suffixes",
        config={
            "parents": subpart_linker_patterns.SUBPART_SUFFIX_PARENTS,
            "children": subpart_linker_patterns.SUBPART_SUFFIX_CHILDREN,
            "weights": consts.TOKEN_WEIGHTS,
            "patterns": matcher_patterns.as_dicts(
                [subpart_linker_patterns.SUBPART_SUFFIX_LINKER]
            ),
        },
    )

    nlp.add_pipe(
        LINK_TRAITS,
        name="link_sex",
        config={
            "parents": sex_linker_patterns.SEX_PARENTS,
            "children": sex_linker_patterns.SEX_CHILDREN,
            "weights": consts.TOKEN_WEIGHTS,
            "patterns": matcher_patterns.as_dicts([sex_linker_patterns.SEX_LINKER]),
        },
    )

    nlp.add_pipe(
        LINK_TRAITS,
        name="link_location",
        config={
            "parents": location_linker_patterns.LOCATION_PARENTS,
            "children": location_linker_patterns.LOCATION_CHILDREN,
            "weights": consts.TOKEN_WEIGHTS,
            "patterns": matcher_patterns.as_dicts(
                [location_linker_patterns.LOCATION_LINKER],
            ),
        },
    )

    nlp.add_pipe(
        LINK_TRAITS,
        name="link_taxa_like",
        config={
            "parents": taxon_like_linker_patterns.TAXON_LIKE_PARENTS,
            "children": taxon_like_linker_patterns.TAXON_LIKE_CHILDREN,
            "weights": consts.TOKEN_WEIGHTS,
            "patterns": matcher_patterns.as_dicts(
                [taxon_like_linker_patterns.TAXON_LIKE_LINKER]
            ),
        },
    )

    # debug_pipes.ents(nlp)  # #######################################################
    # debug_pipes.tokens(nlp)  # #####################################################

    nlp.add_pipe(
        DELETE_TRAITS,
        name="forget_unlinked",
        config={
            "delete": delete_patterns.DELETE_UNLINKED,
            "delete_when": delete_patterns.DELETE_WHEN,
        },
    )

    return nlp
