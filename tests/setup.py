from traiter.pylib.util import shorten

from plants.pylib import sentence_pipeline
from plants.pylib.pipeline_builder import PipelineBuilder

# Singleton for testing
PIPELINE = PipelineBuilder()
PIPELINE.add_tokenizer_pipe()
PIPELINE.add_term_pipe()
PIPELINE.add_range_pipe()
PIPELINE.add_parts_pipe()
PIPELINE.add_simple_traits_pipe()
PIPELINE.add_numeric_traits_pipe()
PIPELINE.add_part_locations_pipe()
# PIPELINE.add_debug_ents_pipe()  # #########################################
# PIPELINE.add_debug_tokens_pipe()  # #########################################
PIPELINE.add_taxa_pipe()
PIPELINE.add_taxon_like_pipe()
PIPELINE.add_group_traits_pipe()
PIPELINE.add_delete_partial_traits_pipe()
PIPELINE.add_merge_pipe()
PIPELINE.add_link_parts_pipe()
PIPELINE.add_link_parts_once_pipe()
PIPELINE.add_link_subparts_pipe()
PIPELINE.add_link_subparts_suffixes_pipe()
PIPELINE.add_link_sex_pipe()
PIPELINE.add_link_location_pipe()
PIPELINE.add_link_taxa_like_pipe()
PIPELINE.add_delete_unlinked_pipe()

SENT_NLP = sentence_pipeline.pipeline()  # Singleton for testing


def test(text: str) -> list[dict]:
    """Find entities in the doc."""
    text = shorten(text)
    doc = PIPELINE(text)
    traits = [e._.data for e in doc.ents]

    # from pprint import pp
    # pp(traits, compact=True)

    # from spacy import displacy
    # displacy.serve(doc, options={'collapse_punct': False, 'compact': True})

    return traits
