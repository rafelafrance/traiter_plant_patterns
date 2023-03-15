from traiter.pylib.util import shorten

from plants.pylib.patterns.term import BASIC_TERMS
from plants.pylib.pipeline_builder import PipelineBuilder

# Singleton for testing
PIPELINE = PipelineBuilder(exclude=["ner"])
PIPELINE.add_tokenizer_pipe()
PIPELINE.add_taxon_terms(before="parser")
PIPELINE.add_basic_terms(BASIC_TERMS, after="parser")
PIPELINE.add_range_patterns()
PIPELINE.add_parts_patterns()
PIPELINE.add_simple_patterns()
PIPELINE.add_numeric_patterns()
PIPELINE.add_part_locations_patterns()
# PIPELINE.add_debug_tokens_pipe()  # #########################################
PIPELINE.add_taxa_patterns()
PIPELINE.add_taxon_plus_patterns(n=2)
PIPELINE.add_taxon_like_patterns()
PIPELINE.add_color_patterns()
PIPELINE.add_group_traits_patterns()
PIPELINE.add_delete_partial_traits_patterns()
PIPELINE.add_merge_pipe()
PIPELINE.add_link_parts_patterns()
PIPELINE.add_link_parts_once_patterns()
PIPELINE.add_link_subparts_patterns()
PIPELINE.add_link_subparts_suffixes_patterns()
PIPELINE.add_link_sex_patterns()
PIPELINE.add_link_location_patterns()
PIPELINE.add_link_taxa_like_patterns()
PIPELINE.add_delete_unlinked_patterns()


def test(text: str) -> list[dict]:
    text = shorten(text)
    doc = PIPELINE(text)
    traits = [e._.data for e in doc.ents]

    # from pprint import pp
    # pp(traits, compact=True)

    return traits
