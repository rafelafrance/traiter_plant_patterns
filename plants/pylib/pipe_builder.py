from traiter.pylib import const as t_const
from traiter.pylib import pipeline_builder

from . import const
from . import tokenizer
from .patterns import count_suffixes
from .patterns import counts
from .patterns import habits
from .patterns import locations_linker
from .patterns import margins
from .patterns import part_locations
from .patterns import parts
from .patterns import parts_linker
from .patterns import ranges
from .patterns import sexes
from .patterns import sexes_linker
from .patterns import shapes
from .patterns import sizes
from .patterns import subparts
from .patterns import subparts_linker
from .patterns import taxa
from .patterns import taxa_like
from .patterns import taxa_like_linker
from .patterns import taxa_plus1
from .patterns import taxa_plus2


class PipeBuilder(pipeline_builder.PipelineBuilder):
    def tokenizer(self):
        tokenizer.setup_tokenizer(self.nlp)

    def taxon_terms(self, **kwargs) -> str:
        prev = self.add_terms(
            const.BINOMIAL_TERMS + const.RANK_TERMS, name="taxon_binomials", **kwargs
        )
        return self.add_terms(
            const.MONOMIAL_TERMS, name=f"taxon_monomials", after=prev, merge=True
        )

    def taxa(self, n=2, **kwargs) -> str:
        prev = self.add_traits(
            [
                taxa.MONOMIAL,
                taxa.SPECIES_TAXON,
                taxa.SUBSPECIES_TAXON,
                taxa.VARIETY_TAXON,
                taxa.SUBVARIETY_TAXON,
                taxa.FORM_TAXON,
                taxa.SUBFORM_TAXON,
                taxa.BAD_TAXON,
            ],
            name="taxa",
            merge=True,
            **kwargs,
        )

        name = "taxa_plus1"
        prev = self.add_traits(
            [taxa_plus1.TAXON_AUTH1, taxa_plus1.MULTI_TAXON],
            name=name,
            merge=True,
            after=prev,
        )

        for i in range(2, n + 1):
            name = f"taxa_plus{i}"
            prev = self.add_traits(
                [taxa_plus2.TAXON_PLUS2], name=name, merge=True, after=prev
            )

        name = "taxa_lower"
        self.add_traits([taxa_plus1.LOWER_MONOMIAL], name=name, after=prev, merge=True)

        return name

    def plant_terms(self, **kwargs) -> str:
        return self.add_terms(
            const.PLANT_TERMS,
            name="plant_terms",
            replace=const.PLANT_TERMS.pattern_dict("replace"),
            merge=True,
            **kwargs,
        )

    def parts(self, **kwargs) -> str:
        return self.add_traits(
            [
                parts.PART,
                parts.MULTIPLE_PARTS,
                parts.MISSING_PART,
                subparts.SUBPART,
                subparts.SUBPART_SUFFIX,
            ],
            name="parts",
            **kwargs,
        )

    def numerics(self, **kwargs) -> str:
        name = self.add_traits(
            [
                ranges.RANGE_LOW,
                ranges.RANGE_MIN_LOW,
                ranges.RANGE_LOW_HIGH,
                ranges.RANGE_LOW_MAX,
                ranges.RANGE_MIN_LOW_HIGH,
                ranges.RANGE_MIN_LOW_MAX,
                ranges.RANGE_LOW_HIGH_MAX,
                ranges.RANGE_MIN_LOW_HIGH_MAX,
                ranges.NOT_A_RANGE,
            ],
            name="ranges",
            merge=True,
            **kwargs,
        )
        return self.add_traits(
            [
                sizes.SIZE,
                sizes.SIZE_HIGH_ONLY,
                sizes.SIZE_DOUBLE_DIM,
                sizes._NOT_A_SIZE,
                counts.COUNT,
                counts.COUNT_WORD,
                counts.NOT_A_COUNT,
                count_suffixes.COUNT_SUFFIX,
                count_suffixes.COUNT_SUFFIX_WORD,
            ],
            name="numerics",
            after=name,
        )

    def taxa_like(self, **kwargs) -> str:
        return self.add_traits([taxa_like.TAXON_LIKE], name="taxon_like", **kwargs)

    def margins(self, **kwargs) -> str:
        return self.add_traits([margins.MARGIN], name="margins", **kwargs)

    def shapes(self, **kwargs) -> str:
        return self.add_traits([shapes.N_SHAPE, shapes.SHAPE], name="shapes", **kwargs)

    def sex(self, **kwargs) -> str:
        return self.add_traits([sexes.SEX], name="sex", **kwargs)

    def part_location(self, **kwargs) -> str:
        return self.add_traits(
            [
                part_locations.PART_AS_DISTANCE,
                part_locations.PART_AS_LOCATION,
                part_locations.SUBPART_AS_LOCATION,
            ],
            name="part_location",
            **kwargs,
        )

    def habits(self, **kwargs) -> str:
        return self.add_traits([habits.HABIT], name="habits", **kwargs)

    def link_parts(self, **kwargs) -> str:
        return self.add_links(
            [parts_linker.PART_LINKER],
            name="link_parts",
            parents=parts_linker._PART_PARENTS,
            children=parts_linker._PART_CHILDREN,
            weights=t_const.TOKEN_WEIGHTS,
            reverse_weights=t_const.REVERSE_WEIGHTS,
            **kwargs,
        )

    def link_parts_once(self, **kwargs) -> str:
        return self.add_links(
            patterns=[parts_linker.LINK_PART_ONCE],
            name="link_parts_once",
            parents=parts_linker._LINK_PART_ONCE_PARENTS,
            children=parts_linker._LINK_PART_ONCE_CHILDREN,
            weights=t_const.TOKEN_WEIGHTS,
            max_links=1,
            differ=["sex", "dimensions"],
            **kwargs,
        )

    def link_subparts(self, **kwargs) -> str:
        return self.add_links(
            [subparts_linker.SUBPART_LINKER],
            name="link_subparts",
            parents=subparts_linker._SUBPART_PARENTS,
            children=subparts_linker._SUBPART_CHILDREN,
            weights=t_const.TOKEN_WEIGHTS,
            **kwargs,
        )

    def link_subparts_suffixes(self, **kwargs) -> str:
        return self.add_links(
            [subparts_linker.SUBPART_SUFFIX_LINKER],
            name="link_subparts_suffixes",
            parents=subparts_linker._SUBPART_SUFFIX_PARENTS,
            children=subparts_linker._SUBPART_SUFFIX_CHILDREN,
            weights=t_const.TOKEN_WEIGHTS,
            **kwargs,
        )

    def link_sex(self, **kwargs) -> str:
        return self.add_links(
            [sexes_linker.SEX_LINKER],
            name="link_sex",
            parents=sexes_linker._SEX_PARENTS,
            children=sexes_linker._SEX_CHILDREN,
            weights=t_const.TOKEN_WEIGHTS,
            **kwargs,
        )

    def link_locations(self, **kwargs) -> str:
        return self.add_links(
            [locations_linker.LOCATION_LINKER],
            name="link_location",
            parents=locations_linker._LOCATION_PARENTS,
            children=locations_linker._LOCATION_CHILDREN,
            weights=t_const.TOKEN_WEIGHTS,
            **kwargs,
        )

    def link_taxa_like(self, name="link_taxa_like", **kwargs) -> str:
        return self.add_links(
            [taxa_like_linker.TAXON_LIKE_LINKER],
            name=name,
            parents=taxa_like_linker._TAXON_LIKE_PARENTS,
            children=taxa_like_linker._TAXON_LIKE_CHILDREN,
            weights=t_const.TOKEN_WEIGHTS,
            **kwargs,
        )
