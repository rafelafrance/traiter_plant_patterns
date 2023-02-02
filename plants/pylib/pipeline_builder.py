import spacy
from traiter.pylib.patterns import matcher_patterns
from traiter.pylib.pipes import debug_pipes
from traiter.pylib.pipes.add_traits_pipe import ADD_TRAITS
from traiter.pylib.pipes.delete_traits_pipe import DELETE_TRAITS
from traiter.pylib.pipes.link_traits_pipe import LINK_TRAITS
from traiter.pylib.pipes.merge_traits import MERGE_TRAITS
from traiter.pylib.pipes.simple_traits_pipe import SIMPLE_TRAITS
from traiter.pylib.pipes.term_pipe import TERM_PIPE

from . import const
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


class PipelineBuilder:
    def __init__(self, trained_pipeline="en_core_web_sm"):
        self.nlp = spacy.load(trained_pipeline, exclude=["ner"])

    def __call__(self, text):
        return self.nlp(text)

    def add_tokenizer_pipe(self):
        tokenizer.setup_tokenizer(self.nlp)

    def add_term_pipe(self, terms=None, replace=None):
        if terms is None:
            terms = term_patterns.TERMS.terms
        if replace is None:
            replace = term_patterns.REPLACE

        self.nlp.add_pipe(
            TERM_PIPE,
            before="parser",
            config={"terms": terms, "replace": replace},
        )
        self.nlp.add_pipe("merge_entities", name="merge_terms")

    def add_range_pipe(self):
        self.nlp.add_pipe(
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
        self.nlp.add_pipe("merge_entities")

    def add_parts_pipe(self):
        self.nlp.add_pipe(
            ADD_TRAITS,
            name="parts",
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

    def add_simple_traits_pipe(self):
        self.nlp.add_pipe(
            SIMPLE_TRAITS,
            config={
                "replace": term_patterns.REPLACE,
                "exclude": ["multiple_parts", "subpart_suffix"],
            },
        )

    def add_numeric_traits_pipe(self):
        self.nlp.add_pipe(
            ADD_TRAITS,
            name="numeric_traits",
            config={
                "patterns": matcher_patterns.as_dicts(
                    [
                        size_patterns.SIZE,
                        size_patterns.SIZE_HIGH_ONLY,
                        size_patterns.SIZE_DOUBLE_DIM,
                        size_patterns.NOT_A_SIZE,
                        count_patterns.COUNT,
                        count_patterns.COUNT_WORD,
                        count_patterns.NOT_A_COUNT,
                        count_suffix_patterns.COUNT_SUFFIX,
                        count_suffix_patterns.COUNT_SUFFIX_WORD,
                    ]
                )
            },
        )

    def add_part_locations_pipe(self):
        self.nlp.add_pipe(
            ADD_TRAITS,
            name="part_locations_traits",
            config={
                "patterns": matcher_patterns.as_dicts(
                    [
                        part_location_patterns.PART_AS_DISTANCE,
                    ]
                )
            },
        )

    def add_taxa_pipe(self):
        self.nlp.add_pipe(
            ADD_TRAITS,
            name="taxa_traits",
            config={
                "patterns": matcher_patterns.as_dicts(
                    [
                        taxon_patterns.TAXON,
                        taxon_patterns.MULTI_TAXON,
                    ]
                )
            },
        )

    def add_taxon_like_pipe(self):
        self.nlp.add_pipe(
            ADD_TRAITS,
            name="taxon_like",
            config={
                "patterns": matcher_patterns.as_dicts([taxon_like_patterns.TAXON_LIKE])
            },
        )

    def add_group_traits_pipe(self):
        self.nlp.add_pipe(
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

    def add_delete_partial_traits_pipe(self, name=DELETE_TRAITS, partial_traits=None):
        if partial_traits is None:
            partial_traits = delete_patterns.PARTIAL_TRAITS
        self.nlp.add_pipe(DELETE_TRAITS, name=name, config={"delete": partial_traits})

    def add_merge_pipe(self):
        self.nlp.add_pipe(MERGE_TRAITS)

    def add_link_parts_pipe(self):
        self.nlp.add_pipe(
            LINK_TRAITS,
            name="link_parts",
            config={
                "parents": part_linker_patterns.PART_PARENTS,
                "children": part_linker_patterns.PART_CHILDREN,
                "weights": const.TOKEN_WEIGHTS,
                "reverse_weights": const.REVERSE_WEIGHTS,
                "patterns": matcher_patterns.as_dicts(
                    [part_linker_patterns.PART_LINKER]
                ),
            },
        )

    def add_link_parts_once_pipe(self):
        self.nlp.add_pipe(
            LINK_TRAITS,
            name="link_parts_once",
            config={
                "parents": part_linker_patterns.LINK_PART_ONCE_PARENTS,
                "children": part_linker_patterns.LINK_PART_ONCE_CHILDREN,
                "weights": const.TOKEN_WEIGHTS,
                "max_links": 1,
                "differ": ["sex", "dimensions"],
                "patterns": matcher_patterns.as_dicts(
                    [part_linker_patterns.LINK_PART_ONCE]
                ),
            },
        )

    def add_link_subparts_pipe(self):
        self.nlp.add_pipe(
            LINK_TRAITS,
            name="link_subparts",
            config={
                "parents": subpart_linker_patterns.SUBPART_PARENTS,
                "children": subpart_linker_patterns.SUBPART_CHILDREN,
                "weights": const.TOKEN_WEIGHTS,
                "patterns": matcher_patterns.as_dicts(
                    [subpart_linker_patterns.SUBPART_LINKER]
                ),
            },
        )

    def add_link_subparts_suffixes_pipe(self):
        self.nlp.add_pipe(
            LINK_TRAITS,
            name="link_subparts_suffixes",
            config={
                "parents": subpart_linker_patterns.SUBPART_SUFFIX_PARENTS,
                "children": subpart_linker_patterns.SUBPART_SUFFIX_CHILDREN,
                "weights": const.TOKEN_WEIGHTS,
                "patterns": matcher_patterns.as_dicts(
                    [subpart_linker_patterns.SUBPART_SUFFIX_LINKER]
                ),
            },
        )

    def add_link_sex_pipe(self):
        self.nlp.add_pipe(
            LINK_TRAITS,
            name="link_sex",
            config={
                "parents": sex_linker_patterns.SEX_PARENTS,
                "children": sex_linker_patterns.SEX_CHILDREN,
                "weights": const.TOKEN_WEIGHTS,
                "patterns": matcher_patterns.as_dicts([sex_linker_patterns.SEX_LINKER]),
            },
        )

    def add_link_location_pipe(self):
        self.nlp.add_pipe(
            LINK_TRAITS,
            name="link_location",
            config={
                "parents": location_linker_patterns.LOCATION_PARENTS,
                "children": location_linker_patterns.LOCATION_CHILDREN,
                "weights": const.TOKEN_WEIGHTS,
                "patterns": matcher_patterns.as_dicts(
                    [location_linker_patterns.LOCATION_LINKER],
                ),
            },
        )

    def add_link_taxa_like_pipe(self):
        self.nlp.add_pipe(
            LINK_TRAITS,
            name="link_taxa_like",
            config={
                "parents": taxon_like_linker_patterns.TAXON_LIKE_PARENTS,
                "children": taxon_like_linker_patterns.TAXON_LIKE_CHILDREN,
                "weights": const.TOKEN_WEIGHTS,
                "patterns": matcher_patterns.as_dicts(
                    [taxon_like_linker_patterns.TAXON_LIKE_LINKER]
                ),
            },
        )

    def add_delete_unlinked_pipe(self, delete_unlinked=None, delete_when=None):
        if delete_when is None:
            delete_unlinked = delete_patterns.DELETE_UNLINKED

        if delete_when is None:
            delete_when = delete_patterns.DELETE_WHEN

        self.nlp.add_pipe(
            DELETE_TRAITS,
            name="delete_unlinked",
            config={"delete": delete_unlinked, "delete_when": delete_when},
        )

    def add_debug_ents_pipe(self):
        debug_pipes.ents(self.nlp)

    def add_debug_tokens_pipe(self):
        debug_pipes.tokens(self.nlp)
