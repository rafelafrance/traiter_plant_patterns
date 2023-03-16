from traiter.pylib import const as t_const
from traiter.pylib import pipeline_builder
from traiter.pylib.pattern_compilers.matcher import Compiler
from traiter.pylib.pipes.add import ADD_TRAITS
from traiter.pylib.pipes.delete import DELETE_TRAITS
from traiter.pylib.pipes.link import LINK_TRAITS
from traiter.pylib.pipes.merge import MERGE_TRAITS
from traiter.pylib.pipes.simple import SIMPLE_TRAITS
from traiter.pylib.pipes.term import TERM_PIPE

from .patterns import count_
from .patterns import count_suffix
from .patterns import delete
from .patterns import habit
from .patterns import location_linker
from .patterns import margin
from .patterns import part
from .patterns import part_linker
from .patterns import part_location
from .patterns import range_
from .patterns import sex_linker
from .patterns import shape
from .patterns import size_
from .patterns import subpart
from .patterns import subpart_linker
from .patterns import taxon
from .patterns import taxon_like
from .patterns import taxon_like_linker
from .patterns import taxon_plus1
from .patterns import taxon_plus2
from .patterns import terms


class PipelineBuilder(pipeline_builder.PipelineBuilder):
    def taxon_terms(self, **kwargs):
        self.nlp.add_pipe(
            TERM_PIPE,
            name="binomial_terms",
            before="ner",
            **kwargs,
            config={"terms": terms.BINOMIAL_TERMS.data + terms.RANK_TERMS.data},
        )
        self.nlp.add_pipe(
            TERM_PIPE,
            name="monomial_terms",
            before="ner",
            config={"terms": terms.MONOMIAL_TERMS.data},
        )
        self.nlp.add_pipe("merge_entities", name="merge_taxon_terms", before="ner")

    def taxa(self, **kwargs):
        self.nlp.add_pipe(
            ADD_TRAITS,
            name="taxa",
            before="ner",
            **kwargs,
            config={
                "patterns": Compiler.as_dicts(
                    [
                        taxon.MONOMIAL,
                        taxon.SPECIES_TAXON,
                        taxon.SUBSPECIES_TAXON,
                        taxon.VARIETY_TAXON,
                        taxon.SUBVARIETY_TAXON,
                        taxon.FORM_TAXON,
                        taxon.SUBFORM_TAXON,
                        taxon.BAD_TAXON,
                    ]
                )
            },
        )
        self.nlp.add_pipe("merge_entities", name="taxon_merge", before="ner")

    def taxon_plus(self, n=1, **kwargs):
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
            name="taxon_plus1",
            before="ner",
            **kwargs,
            config={
                "patterns": Compiler.as_dicts(
                    [
                        taxon_plus1.TAXON_PLUS1,
                        taxon_plus1.MULTI_TAXON,
                    ]
                )
            },
        )
        self.nlp.add_pipe(
            "merge_entities",
            name="taxon_plus1_merge",
            before="ner",
        )

        for i in range(2, n + 1):
            name_add = f"taxon_plus{i}"
            name_merge = f"taxon_plus_merge{i}"

            self.nlp.add_pipe(
                ADD_TRAITS,
                name=name_add,
                before="ner",
                config={"patterns": Compiler.as_dicts([taxon_plus2.TAXON_PLUS2])},
            )
            self.nlp.add_pipe("merge_entities", name=name_merge, before="ner")

    def plant_terms(self, term_list=None, **kwargs):
        term_list = term_list if term_list else terms.PLANT_TERMS.data
        self.nlp.add_pipe(
            TERM_PIPE,
            name="plant_terms",
            **kwargs,
            config={"terms": term_list},
        )
        self.nlp.add_pipe(
            "merge_entities", name="plant_terms_merge", after="plant_terms"
        )

    def ranges(self, **kwargs):
        self.nlp.add_pipe(
            ADD_TRAITS,
            name="range",
            **kwargs,
            config={
                "patterns": Compiler.as_dicts(
                    [
                        range_.RANGE_LOW,
                        range_.RANGE_MIN_LOW,
                        range_.RANGE_LOW_HIGH,
                        range_.RANGE_LOW_MAX,
                        range_.RANGE_MIN_LOW_HIGH,
                        range_.RANGE_MIN_LOW_MAX,
                        range_.RANGE_LOW_HIGH_MAX,
                        range_.RANGE_MIN_LOW_HIGH_MAX,
                        range_.NOT_A_RANGE,
                    ]
                )
            },
        )
        self.nlp.add_pipe("merge_entities", name="range_merge")

    def parts(self, **kwargs):
        self.nlp.add_pipe(
            ADD_TRAITS,
            name="parts",
            **kwargs,
            config={
                "patterns": Compiler.as_dicts(
                    [
                        part.PART,
                        part.MISSING_PART,
                        subpart.SUBPART,
                        subpart.SUBPART_SUFFIX,
                    ]
                )
            },
        )

    def simple(self, **kwargs):
        self.nlp.add_pipe(
            SIMPLE_TRAITS,
            **kwargs,
            config={
                "exclude": ["multiple_parts", "subpart_suffix"],
            },
        )

    def numeric(self, **kwargs):
        self.nlp.add_pipe(
            ADD_TRAITS,
            name="numeric_traits",
            **kwargs,
            config={
                "patterns": Compiler.as_dicts(
                    [
                        size_.SIZE,
                        size_.SIZE_HIGH_ONLY,
                        size_.SIZE_DOUBLE_DIM,
                        size_._NOT_A_SIZE,
                        count_.COUNT,
                        count_.COUNT_WORD,
                        count_.NOT_A_COUNT,
                        count_suffix.COUNT_SUFFIX,
                        count_suffix.COUNT_SUFFIX_WORD,
                    ]
                )
            },
        )

    def part_locations(self, **kwargs):
        self.nlp.add_pipe(
            ADD_TRAITS,
            name="part_locations_traits",
            **kwargs,
            config={
                "patterns": Compiler.as_dicts(
                    [
                        part_location.PART_AS_DISTANCE,
                    ]
                )
            },
        )

    def taxon_like(self, **kwargs):
        self.nlp.add_pipe(
            ADD_TRAITS,
            name="taxon_like",
            **kwargs,
            config={"patterns": Compiler.as_dicts([taxon_like.TAXON_LIKE])},
        )

    def group_traits(self, **kwargs):
        self.nlp.add_pipe(
            ADD_TRAITS,
            name="group_traits",
            **kwargs,
            config={
                "patterns": Compiler.as_dicts(
                    [
                        margin.MARGIN,
                        shape.N_SHAPE,
                        shape.SHAPE,
                        part_location.PART_AS_LOCATION,
                        part_location.SUBPART_AS_LOCATION,
                        habit.HABIT,
                    ]
                )
            },
        )

    def delete_partial_traits(self, name=DELETE_TRAITS, partial_traits=None, **kwargs):
        if partial_traits is None:
            partial_traits = delete.PARTIAL_TRAITS
        self.nlp.add_pipe(
            DELETE_TRAITS, name=name, **kwargs, config={"delete": partial_traits}
        )

    def merge_pipe(self, **kwargs):
        self.nlp.add_pipe(MERGE_TRAITS, **kwargs)

    def link_parts(self):
        self.nlp.add_pipe(
            LINK_TRAITS,
            name="link_parts",
            config={
                "parents": part_linker._PART_PARENTS,
                "children": part_linker._PART_CHILDREN,
                "weights": t_const.TOKEN_WEIGHTS,
                "reverse_weights": t_const.REVERSE_WEIGHTS,
                "patterns": Compiler.as_dicts([part_linker.PART_LINKER]),
            },
        )

    def link_parts_once(self, **kwargs):
        self.nlp.add_pipe(
            LINK_TRAITS,
            name="link_parts_once",
            **kwargs,
            config={
                "parents": part_linker._LINK_PART_ONCE_PARENTS,
                "children": part_linker._LINK_PART_ONCE_CHILDREN,
                "weights": t_const.TOKEN_WEIGHTS,
                "max_links": 1,
                "differ": ["sex", "dimensions"],
                "patterns": Compiler.as_dicts([part_linker.LINK_PART_ONCE]),
            },
        )

    def link_subparts(self, **kwargs):
        self.nlp.add_pipe(
            LINK_TRAITS,
            name="link_subparts",
            **kwargs,
            config={
                "parents": subpart_linker._SUBPART_PARENTS,
                "children": subpart_linker._SUBPART_CHILDREN,
                "weights": t_const.TOKEN_WEIGHTS,
                "patterns": Compiler.as_dicts([subpart_linker.SUBPART_LINKER]),
            },
        )

    def link_subparts_suffixes(self, **kwargs):
        self.nlp.add_pipe(
            LINK_TRAITS,
            name="link_subparts_suffixes",
            **kwargs,
            config={
                "parents": subpart_linker._SUBPART_SUFFIX_PARENTS,
                "children": subpart_linker._SUBPART_SUFFIX_CHILDREN,
                "weights": t_const.TOKEN_WEIGHTS,
                "patterns": Compiler.as_dicts([subpart_linker.SUBPART_SUFFIX_LINKER]),
            },
        )

    def link_sex(self, **kwargs):
        self.nlp.add_pipe(
            LINK_TRAITS,
            name="link_sex",
            **kwargs,
            config={
                "parents": sex_linker._SEX_PARENTS,
                "children": sex_linker._SEX_CHILDREN,
                "weights": t_const.TOKEN_WEIGHTS,
                "patterns": Compiler.as_dicts([sex_linker.SEX_LINKER]),
            },
        )

    def link_location(self, **kwargs):
        self.nlp.add_pipe(
            LINK_TRAITS,
            name="link_location",
            **kwargs,
            config={
                "parents": location_linker._LOCATION_PARENTS,
                "children": location_linker._LOCATION_CHILDREN,
                "weights": t_const.TOKEN_WEIGHTS,
                "patterns": Compiler.as_dicts(
                    [location_linker.LOCATION_LINKER],
                ),
            },
        )

    def link_taxa_like(self, **kwargs):
        self.nlp.add_pipe(
            LINK_TRAITS,
            name="link_taxa_like",
            **kwargs,
            config={
                "parents": taxon_like_linker._TAXON_LIKE_PARENTS,
                "children": taxon_like_linker._TAXON_LIKE_CHILDREN,
                "weights": t_const.TOKEN_WEIGHTS,
                "patterns": Compiler.as_dicts([taxon_like_linker.TAXON_LIKE_LINKER]),
            },
        )

    def delete_unlinked(self, delete_unlinked=None, delete_when=None, **kwargs):
        if delete_unlinked is None:
            delete_unlinked = delete.PARTIAL_TRAITS

        if delete_when is None:
            delete_when = delete.DELETE_WHEN

        self.nlp.add_pipe(
            DELETE_TRAITS,
            name="delete_unlinked",
            **kwargs,
            config={"delete": delete_unlinked, "delete_when": delete_when},
        )
