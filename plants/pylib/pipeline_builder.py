from traiter.pylib import const as t_const
from traiter.pylib import pipeline_builder
from traiter.pylib.pattern_compilers import matcher_compiler
from traiter.pylib.pipes import debug_pipes
from traiter.pylib.pipes.add_traits_pipe import ADD_TRAITS
from traiter.pylib.pipes.delete_traits_pipe import DELETE_TRAITS
from traiter.pylib.pipes.link_traits_pipe import LINK_TRAITS
from traiter.pylib.pipes.merge_traits import MERGE_TRAITS
from traiter.pylib.pipes.simple_traits_pipe import SIMPLE_TRAITS
from traiter.pylib.pipes.term_pipe import TERM_PIPE

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
from .patterns import taxon_plus_patterns1
from .patterns import taxon_plus_patterns2
from .patterns import term_patterns


class PipelineBuilder(pipeline_builder.PipelineBuilder):
    def add_taxon_terms(self, **kwargs):
        self.nlp.add_pipe(
            TERM_PIPE,
            name="binomial_terms",
            **kwargs,
            config={"terms": term_patterns.BINOMIAL_TERMS},
        )
        self.nlp.add_pipe(
            TERM_PIPE,
            name="monomial_terms",
            after="binomial_terms",
            config={"terms": term_patterns.MONOMIAL_TERMS},
        )
        self.nlp.add_pipe(
            "merge_entities", name="merge_taxon_terms", after="monomial_terms"
        )

    def add_basic_terms(self, terms, **kwargs):
        self.nlp.add_pipe(
            TERM_PIPE,
            name="basic_terms",
            **kwargs,
            config={"terms": terms},
        )
        self.nlp.add_pipe(
            "merge_entities", name="merge_basic_terms", after="basic_terms"
        )

    def add_range_patterns(self, **kwargs):
        self.nlp.add_pipe(
            ADD_TRAITS,
            name="range_pipe",
            **kwargs,
            config={
                "patterns": matcher_compiler.as_dicts(
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

    def add_parts_patterns(self, **kwargs):
        self.nlp.add_pipe(
            ADD_TRAITS,
            name="parts",
            **kwargs,
            config={
                "patterns": matcher_compiler.as_dicts(
                    [
                        part_patterns.PART,
                        part_patterns.MISSING_PART,
                        subpart_patterns.SUBPART,
                        subpart_patterns.SUBPART_SUFFIX,
                    ]
                )
            },
        )

    def add_simple_patterns(self, **kwargs):
        self.nlp.add_pipe(
            SIMPLE_TRAITS,
            **kwargs,
            config={
                "replace": term_patterns.REPLACE,
                "exclude": ["multiple_parts", "subpart_suffix"],
            },
        )

    def add_numeric_patterns(self, **kwargs):
        self.nlp.add_pipe(
            ADD_TRAITS,
            name="numeric_traits",
            **kwargs,
            config={
                "patterns": matcher_compiler.as_dicts(
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

    def add_part_locations_patterns(self, **kwargs):
        self.nlp.add_pipe(
            ADD_TRAITS,
            name="part_locations_traits",
            **kwargs,
            config={
                "patterns": matcher_compiler.as_dicts(
                    [
                        part_location_patterns.PART_AS_DISTANCE,
                    ]
                )
            },
        )

    def add_taxa_patterns(self, **kwargs):
        self.nlp.add_pipe(
            ADD_TRAITS,
            name="taxon_traits",
            **kwargs,
            config={
                "patterns": matcher_compiler.as_dicts(
                    [
                        taxon_patterns.MONOMIAL,
                        taxon_patterns.SPECIES_TAXON,
                        taxon_patterns.SUBSPECIES_TAXON,
                        taxon_patterns.VARIETY_TAXON,
                        taxon_patterns.SUBVARIETY_TAXON,
                        taxon_patterns.FORM_TAXON,
                        taxon_patterns.SUBFORM_TAXON,
                        taxon_patterns.BAD_TAXON,
                    ]
                )
            },
        )
        self.nlp.add_pipe("merge_entities", name="merge_taxa", after="taxon_traits")

    def add_taxon_plus_patterns(self, n=1, **kwargs):
        """Get taxon patterns that are build up from previous taxon notations:

        a) A taxon with an authority like: "Canis lupus Lineus". The authority is Lineus
        b) Multiple taxa like: "Mimosa sensitiva and Canis lupus".
        c) Not a taxon like: "Rio Platanillo". Some locations or names overlap with
           higher taxa.

        Use the n parameter to build up taxa with authorities at multiple ranks.

        1 if your taxa have at maximum one citation per taxon like:
            "Canis lupus Lineus"
            "Lineus" is the single authority.

        2 if you may have 2 citations per taxon like:
            "Vicia villosa Roth ssp. varia (Khan)"
            The species authority is "Roth" and the subspecies authority is "Khan".
            The taxon rank is subspecies.

        3 if you have up to 3 citations in a taxon like:
            "Mimosa gracilis Barneby subsp. capillipes Khan var. brevissima (Bozo)"
            Three authorities: Barneby, Khan, and Bozo. The rank here is variant.
        """
        self.nlp.add_pipe(
            ADD_TRAITS,
            name="taxon_plus_traits1",
            **kwargs,
            config={
                "patterns": matcher_compiler.as_dicts(
                    [
                        taxon_plus_patterns1.TAXON_PLUS1,
                        taxon_plus_patterns1.MULTI_TAXON,
                    ]
                )
            },
        )
        self.nlp.add_pipe(
            "merge_entities",
            name="taxon_plus_merge_traits1",
            after="taxon_plus_traits1",
        )

        prev_name_merge = "taxon_plus_merge_traits1"

        for i in range(2, n + 1):
            name_add = f"taxon_plus_traits{i}"
            name_merge = f"taxon_plus_merge_traits{i}"

            self.nlp.add_pipe(
                ADD_TRAITS,
                name=name_add,
                after=prev_name_merge,
                config={
                    "patterns": matcher_compiler.as_dicts(
                        [taxon_plus_patterns2.TAXON_PLUS2]
                    )
                },
            )

            self.nlp.add_pipe("merge_entities", name=name_merge, after=name_add)
            prev_name_merge = name_merge

    def add_taxon_like_patterns(self, **kwargs):
        self.nlp.add_pipe(
            ADD_TRAITS,
            name="taxon_like",
            **kwargs,
            config={
                "patterns": matcher_compiler.as_dicts([taxon_like_patterns.TAXON_LIKE])
            },
        )

    def add_group_traits_patterns(self, **kwargs):
        self.nlp.add_pipe(
            ADD_TRAITS,
            name="group_traits",
            **kwargs,
            config={
                "patterns": matcher_compiler.as_dicts(
                    [
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

    def add_delete_partial_traits_patterns(
        self, name=DELETE_TRAITS, partial_traits=None, **kwargs
    ):
        if partial_traits is None:
            partial_traits = delete_patterns.PARTIAL_TRAITS
        self.nlp.add_pipe(
            DELETE_TRAITS, name=name, **kwargs, config={"delete": partial_traits}
        )

    def add_merge_pipe(self, **kwargs):
        self.nlp.add_pipe(MERGE_TRAITS, **kwargs)

    def add_link_parts_patterns(self):
        self.nlp.add_pipe(
            LINK_TRAITS,
            name="link_parts",
            config={
                "parents": part_linker_patterns.PART_PARENTS,
                "children": part_linker_patterns.PART_CHILDREN,
                "weights": t_const.TOKEN_WEIGHTS,
                "reverse_weights": t_const.REVERSE_WEIGHTS,
                "patterns": matcher_compiler.as_dicts(
                    [part_linker_patterns.PART_LINKER]
                ),
            },
        )

    def add_link_parts_once_patterns(self, **kwargs):
        self.nlp.add_pipe(
            LINK_TRAITS,
            name="link_parts_once",
            **kwargs,
            config={
                "parents": part_linker_patterns.LINK_PART_ONCE_PARENTS,
                "children": part_linker_patterns.LINK_PART_ONCE_CHILDREN,
                "weights": t_const.TOKEN_WEIGHTS,
                "max_links": 1,
                "differ": ["sex", "dimensions"],
                "patterns": matcher_compiler.as_dicts(
                    [part_linker_patterns.LINK_PART_ONCE]
                ),
            },
        )

    def add_link_subparts_patterns(self, **kwargs):
        self.nlp.add_pipe(
            LINK_TRAITS,
            name="link_subparts",
            **kwargs,
            config={
                "parents": subpart_linker_patterns.SUBPART_PARENTS,
                "children": subpart_linker_patterns.SUBPART_CHILDREN,
                "weights": t_const.TOKEN_WEIGHTS,
                "patterns": matcher_compiler.as_dicts(
                    [subpart_linker_patterns.SUBPART_LINKER]
                ),
            },
        )

    def add_link_subparts_suffixes_patterns(self, **kwargs):
        self.nlp.add_pipe(
            LINK_TRAITS,
            name="link_subparts_suffixes",
            **kwargs,
            config={
                "parents": subpart_linker_patterns.SUBPART_SUFFIX_PARENTS,
                "children": subpart_linker_patterns.SUBPART_SUFFIX_CHILDREN,
                "weights": t_const.TOKEN_WEIGHTS,
                "patterns": matcher_compiler.as_dicts(
                    [subpart_linker_patterns.SUBPART_SUFFIX_LINKER]
                ),
            },
        )

    def add_link_sex_patterns(self, **kwargs):
        self.nlp.add_pipe(
            LINK_TRAITS,
            name="link_sex",
            **kwargs,
            config={
                "parents": sex_linker_patterns.SEX_PARENTS,
                "children": sex_linker_patterns.SEX_CHILDREN,
                "weights": t_const.TOKEN_WEIGHTS,
                "patterns": matcher_compiler.as_dicts([sex_linker_patterns.SEX_LINKER]),
            },
        )

    def add_link_location_patterns(self, **kwargs):
        self.nlp.add_pipe(
            LINK_TRAITS,
            name="link_location",
            **kwargs,
            config={
                "parents": location_linker_patterns.LOCATION_PARENTS,
                "children": location_linker_patterns.LOCATION_CHILDREN,
                "weights": t_const.TOKEN_WEIGHTS,
                "patterns": matcher_compiler.as_dicts(
                    [location_linker_patterns.LOCATION_LINKER],
                ),
            },
        )

    def add_link_taxa_like_patterns(self, **kwargs):
        self.nlp.add_pipe(
            LINK_TRAITS,
            name="link_taxa_like",
            **kwargs,
            config={
                "parents": taxon_like_linker_patterns.TAXON_LIKE_PARENTS,
                "children": taxon_like_linker_patterns.TAXON_LIKE_CHILDREN,
                "weights": t_const.TOKEN_WEIGHTS,
                "patterns": matcher_compiler.as_dicts(
                    [taxon_like_linker_patterns.TAXON_LIKE_LINKER]
                ),
            },
        )

    def add_delete_unlinked_patterns(
        self, delete_unlinked=None, delete_when=None, **kwargs
    ):
        if delete_when is None:
            delete_unlinked = delete_patterns.DELETE_UNLINKED

        if delete_when is None:
            delete_when = delete_patterns.DELETE_WHEN

        self.nlp.add_pipe(
            DELETE_TRAITS,
            name="delete_unlinked",
            **kwargs,
            config={"delete": delete_unlinked, "delete_when": delete_when},
        )

    def add_debug_ents_pipe(self):
        debug_pipes.ents(self.nlp)

    def add_debug_tokens_pipe(self):
        debug_pipes.tokens(self.nlp)
