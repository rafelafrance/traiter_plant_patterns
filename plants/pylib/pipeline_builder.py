from traiter.pylib import const as t_const
from traiter.pylib import pipeline_builder

from . import tokenizer
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
from .patterns import sex
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
    def tokenizer(self):
        tokenizer.setup_tokenizer(self.nlp)

    def taxon_terms(self, name="taxon_terms", **kwargs):
        self.add_terms(terms.BINOMIAL_TERMS + terms.RANK_TERMS, name=name, **kwargs)
        self.add_terms(
            terms.MONOMIAL_TERMS, name=f"{name}_monomial", after=name, merge=True
        )

    def taxa(self, **kwargs):
        self.add_traits(
            [
                taxon.MONOMIAL,
                taxon.SPECIES_TAXON,
                taxon.SUBSPECIES_TAXON,
                taxon.VARIETY_TAXON,
                taxon.SUBVARIETY_TAXON,
                taxon.FORM_TAXON,
                taxon.SUBFORM_TAXON,
                taxon.BAD_TAXON,
            ],
            name="taxa",
            merge=True,
            **kwargs,
        )

    def taxa_plus(self, n=1, **kwargs):
        self.add_traits(
            [taxon_plus1.TAXON_PLUS1, taxon_plus1.MULTI_TAXON],
            name="taxon_plus1",
            merge=True,
            **kwargs,
        )

        for i in range(2, n + 1):
            self.add_traits(
                [taxon_plus2.TAXON_PLUS2], name=f"taxon_plus{i}", merge=True, **kwargs
            )

    def plant_terms(self, name="plant_terms", **kwargs):
        self.add_terms(
            terms.PLANT_TERMS,
            name=name,
            replace=terms.PLANT_TERMS.pattern_dict("replace"),
            merge=True,
            **kwargs,
        )

    def parts(self, **kwargs):
        self.add_traits(
            [
                part.PART,
                part.MULTIPLE_PARTS,
                part.MISSING_PART,
                subpart.SUBPART,
                subpart.SUBPART_SUFFIX,
            ],
            name="parts",
            **kwargs,
        )

    def numerics(self, **kwargs):
        self.add_traits(
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
            ],
            name="ranges",
            merge=True,
            **kwargs,
        )
        self.add_traits(
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
            ],
            name="numerics",
            **kwargs,
        )

    def taxa_like(self, **kwargs):
        self.add_traits([taxon_like.TAXON_LIKE], name="taxon_like", **kwargs)

    def margins(self, **kwargs):
        self.add_traits([margin.MARGIN], name="margins", **kwargs)

    def shapes(self, **kwargs):
        self.add_traits([shape.N_SHAPE, shape.SHAPE], name="shapes", **kwargs)

    def sex(self, **kwargs):
        self.add_traits([sex.SEX], name="sex", **kwargs)

    def part_locations(self, **kwargs):
        self.add_traits(
            [
                part_location.PART_AS_DISTANCE,
                part_location.PART_AS_LOCATION,
                part_location.SUBPART_AS_LOCATION,
            ],
            name="part_location",
            **kwargs,
        )

    def habits(self, **kwargs):
        self.add_traits([habit.HABIT], name="habits", **kwargs)

    def link_parts(self, **kwargs):
        self.add_links(
            [part_linker.PART_LINKER],
            name="link_parts",
            parents=part_linker._PART_PARENTS,
            children=part_linker._PART_CHILDREN,
            weights=t_const.TOKEN_WEIGHTS,
            reverse_weights=t_const.REVERSE_WEIGHTS,
            **kwargs,
        )

    def link_parts_once(self, **kwargs):
        self.add_links(
            patterns=[part_linker.LINK_PART_ONCE],
            name="link_parts_once",
            parents=part_linker._LINK_PART_ONCE_PARENTS,
            children=part_linker._LINK_PART_ONCE_CHILDREN,
            weights=t_const.TOKEN_WEIGHTS,
            max_links=1,
            differ=["sex", "dimensions"],
            **kwargs,
        )

    def link_subparts(self, **kwargs):
        self.add_links(
            [subpart_linker.SUBPART_LINKER],
            name="link_subparts",
            parents=subpart_linker._SUBPART_PARENTS,
            children=subpart_linker._SUBPART_CHILDREN,
            weights=t_const.TOKEN_WEIGHTS,
            **kwargs,
        )

    def link_subparts_suffixes(self, **kwargs):
        self.add_links(
            [subpart_linker.SUBPART_SUFFIX_LINKER],
            name="link_subparts_suffixes",
            parents=subpart_linker._SUBPART_SUFFIX_PARENTS,
            children=subpart_linker._SUBPART_SUFFIX_CHILDREN,
            weights=t_const.TOKEN_WEIGHTS,
            **kwargs,
        )

    def link_sex(self, **kwargs):
        self.add_links(
            [sex_linker.SEX_LINKER],
            name="link_sex",
            parents=sex_linker._SEX_PARENTS,
            children=sex_linker._SEX_CHILDREN,
            weights=t_const.TOKEN_WEIGHTS,
            **kwargs,
        )

    def link_locations(self, **kwargs):
        self.add_links(
            [location_linker.LOCATION_LINKER],
            name="link_location",
            parents=location_linker._LOCATION_PARENTS,
            children=location_linker._LOCATION_CHILDREN,
            weights=t_const.TOKEN_WEIGHTS,
            **kwargs,
        )

    def link_taxa_like(self, name="link_taxa_like", **kwargs):
        self.add_links(
            [taxon_like_linker.TAXON_LIKE_LINKER],
            name=name,
            parents=taxon_like_linker._TAXON_LIKE_PARENTS,
            children=taxon_like_linker._TAXON_LIKE_CHILDREN,
            weights=t_const.TOKEN_WEIGHTS,
            **kwargs,
        )

    def delete_unlinked(self, delete_unlinked=None, delete_when=None, **kwargs):
        if delete_unlinked is None:
            delete_unlinked = delete.PARTIAL_TRAITS

        if delete_when is None:
            delete_when = delete.DELETE_WHEN

        self.delete_traits(
            "delete_unlinked", delete=delete_unlinked, delete_when=delete_when, **kwargs
        )

    def delete_partial_traits(
        self, name="delete_partials", partial_traits=None, **kwargs
    ):
        if partial_traits is None:
            partial_traits = delete.PARTIAL_TRAITS

        self.delete_traits(name=name, delete=partial_traits, **kwargs)
