from traiter.pylib import const as t_const
from traiter.pylib import pipeline_builder
from traiter.pylib.pattern_compilers.matcher import Compiler
from traiter.pylib.pipes.add import ADD_TRAITS
from traiter.pylib.pipes.delete import DELETE_TRAITS
from traiter.pylib.pipes.link import LINK_TRAITS
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
    def taxon_terms(self, name="taxon_terms", **kwargs):
        self.nlp.add_pipe(
            TERM_PIPE,
            name=name,
            **kwargs,
            config={"terms": terms.BINOMIAL_TERMS.data + terms.RANK_TERMS.data},
        )
        self.nlp.add_pipe(
            TERM_PIPE,
            name=f"{name}_monomial",
            after=name,
            config={"terms": terms.MONOMIAL_TERMS.data},
        )
        self.nlp.add_pipe(
            "merge_entities", name=f"{name}_merge", after=f"{name}_monomial"
        )

    def taxa(self, name="taxa", **kwargs):
        self.nlp.add_pipe(
            ADD_TRAITS,
            name=name,
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
        self.nlp.add_pipe("merge_entities", name=f"{name}_merge", after=name)

    def taxon_plus(self, name="taxon_plus1", n=1, **kwargs):
        """Get taxon patterns that are build up from previous taxon notations:

        a) A taxon with an authority like: "Canis lupus Linnaeus".
           The authority is Linnaeus.
        b) Multiple taxa like: "Mimosa sensitiva and Canis lupus".

        Use the n parameter to build up taxa with authorities at multiple ranks.

        1 if your taxa have at maximum one citation per taxon like:
            "Canis lupus Linnaeus"
            "Linnaeus" is the single authority.

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
            name=name,
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
            name=f"{name}1_merge",
            after=name,
        )

        prev = f"{name}1_merge"

        for i in range(2, n + 1):
            name_add = f"name{i}"
            name_merge = f"{name}_merge{i}"

            self.nlp.add_pipe(
                ADD_TRAITS,
                name=name_add,
                after=prev,
                config={"patterns": Compiler.as_dicts([taxon_plus2.TAXON_PLUS2])},
            )
            self.nlp.add_pipe("merge_entities", name=name_merge, after=name_add)
            prev = name_merge

    def plant_terms(self, name="plant_terms", term_list=None, **kwargs):
        term_list = term_list if term_list else terms.PLANT_TERMS.data
        self.nlp.add_pipe(
            TERM_PIPE,
            name=name,
            **kwargs,
            config={"terms": term_list},
        )
        self.nlp.add_pipe("merge_entities", name=f"{name}_merge", after=name)

    def parts(self, name="parts", **kwargs):
        self.nlp.add_pipe(
            ADD_TRAITS,
            name=name,
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

    def parts_plus(self, name="parts_plus", **kwargs):
        self.nlp.add_pipe(
            SIMPLE_TRAITS,
            name=name,
            **kwargs,
            config={
                "exclude": ["multiple_parts", "subpart_suffix"],
            },
        )

    def numerics(self, name="numeric_traits", **kwargs):
        self.nlp.add_pipe(
            ADD_TRAITS,
            **kwargs,
            name=name,
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
        self.nlp.add_pipe("merge_entities", name=f"{name}_merge", after=name)
        self.nlp.add_pipe(
            ADD_TRAITS,
            name=f"{name}_traits",
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

    def taxa_like(self, name="taxon_like", **kwargs):
        self.nlp.add_pipe(
            ADD_TRAITS,
            name=name,
            **kwargs,
            config={"patterns": Compiler.as_dicts([taxon_like.TAXON_LIKE])},
        )

    def margins(self, name="margin", **kwargs):
        self.nlp.add_pipe(
            ADD_TRAITS,
            name=name,
            **kwargs,
            config={"patterns": Compiler.as_dicts([margin.MARGIN])},
        )

    def shapes(self, name="shape", **kwargs):
        self.nlp.add_pipe(
            ADD_TRAITS,
            name=name,
            **kwargs,
            config={"patterns": Compiler.as_dicts([shape.N_SHAPE, shape.SHAPE])},
        )

    def part_locations(self, name="part_location", **kwargs):
        self.nlp.add_pipe(
            ADD_TRAITS,
            name=name,
            **kwargs,
            config={
                "patterns": Compiler.as_dicts(
                    [
                        part_location.PART_AS_DISTANCE,
                        part_location.PART_AS_LOCATION,
                        part_location.SUBPART_AS_LOCATION,
                    ]
                )
            },
        )

    def habits(self, name="habit", **kwargs):
        self.nlp.add_pipe(
            ADD_TRAITS,
            name=name,
            **kwargs,
            config={"patterns": Compiler.as_dicts([habit.HABIT])},
        )

    def delete_partial_traits(
        self, name="delete_partials", partial_traits=None, **kwargs
    ):
        if partial_traits is None:
            partial_traits = delete.PARTIAL_TRAITS
        self.nlp.add_pipe(
            DELETE_TRAITS,
            name=name,
            **kwargs,
            config={"delete": partial_traits},
        )

    def link_parts(self, name="link_parts"):
        self.nlp.add_pipe(
            LINK_TRAITS,
            name=name,
            config={
                "parents": part_linker._PART_PARENTS,
                "children": part_linker._PART_CHILDREN,
                "weights": t_const.TOKEN_WEIGHTS,
                "reverse_weights": t_const.REVERSE_WEIGHTS,
                "patterns": Compiler.as_dicts([part_linker.PART_LINKER]),
            },
        )

    def link_parts_once(self, name="link_parts_once", **kwargs):
        self.nlp.add_pipe(
            LINK_TRAITS,
            name=name,
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

    def link_subparts(self, name="link_subparts", **kwargs):
        self.nlp.add_pipe(
            LINK_TRAITS,
            name=name,
            **kwargs,
            config={
                "parents": subpart_linker._SUBPART_PARENTS,
                "children": subpart_linker._SUBPART_CHILDREN,
                "weights": t_const.TOKEN_WEIGHTS,
                "patterns": Compiler.as_dicts([subpart_linker.SUBPART_LINKER]),
            },
        )

    def link_subparts_suffixes(self, name="link_subparts_suffixes", **kwargs):
        self.nlp.add_pipe(
            LINK_TRAITS,
            name=name,
            **kwargs,
            config={
                "parents": subpart_linker._SUBPART_SUFFIX_PARENTS,
                "children": subpart_linker._SUBPART_SUFFIX_CHILDREN,
                "weights": t_const.TOKEN_WEIGHTS,
                "patterns": Compiler.as_dicts([subpart_linker.SUBPART_SUFFIX_LINKER]),
            },
        )

    def link_sex(self, name="link_sex", **kwargs):
        self.nlp.add_pipe(
            LINK_TRAITS,
            name=name,
            **kwargs,
            config={
                "parents": sex_linker._SEX_PARENTS,
                "children": sex_linker._SEX_CHILDREN,
                "weights": t_const.TOKEN_WEIGHTS,
                "patterns": Compiler.as_dicts([sex_linker.SEX_LINKER]),
            },
        )

    def link_locations(self, name="link_location", **kwargs):
        self.nlp.add_pipe(
            LINK_TRAITS,
            name=name,
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

    def link_taxa_like(self, name="link_taxa_like", **kwargs):
        self.nlp.add_pipe(
            LINK_TRAITS,
            name=name,
            **kwargs,
            config={
                "parents": taxon_like_linker._TAXON_LIKE_PARENTS,
                "children": taxon_like_linker._TAXON_LIKE_CHILDREN,
                "weights": t_const.TOKEN_WEIGHTS,
                "patterns": Compiler.as_dicts([taxon_like_linker.TAXON_LIKE_LINKER]),
            },
        )

    def delete_unlinked(
        self, delete_unlinked=None, delete_when=None, name="delete_unlinked", **kwargs
    ):
        if delete_unlinked is None:
            delete_unlinked = delete.PARTIAL_TRAITS

        if delete_when is None:
            delete_when = delete.DELETE_WHEN

        self.nlp.add_pipe(
            DELETE_TRAITS,
            name=name,
            **kwargs,
            config={"delete": delete_unlinked, "delete_when": delete_when},
        )
