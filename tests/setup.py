from traiter.pylib.util import shorten

from plants.pylib.patterns.delete import PARTIAL_TRAITS
from plants.pylib.pipeline_builder import PipelineBuilder

# Singleton for testing
PIPELINE = PipelineBuilder()
PIPELINE.taxon_terms(before="ner")
PIPELINE.taxa(before="ner")
PIPELINE.taxon_plus(n=2, before="ner")
# PIPELINE.debug_tokens(before="ner")  # ####################################
PIPELINE.plant_terms(before="ner")
# PIPELINE.parts(before="ner")
# PIPELINE.parts_plus(before="ner")
# PIPELINE.numerics(before="ner")
# PIPELINE.part_locations(before="ner")
# PIPELINE.colors(before="ner")
# PIPELINE.add_taxon_like_patterns()
# PIPELINE.add_group_traits_patterns()
# PIPELINE.add_delete_partial_traits_patterns()
# PIPELINE.add_merge_pipe()
# PIPELINE.add_link_parts_patterns()
# PIPELINE.add_link_parts_once_patterns()
# PIPELINE.add_link_subparts_patterns()
# PIPELINE.add_link_subparts_suffixes_patterns()
# PIPELINE.add_link_sex_patterns()
# PIPELINE.add_link_location_patterns()
# PIPELINE.add_link_taxa_like_patterns()
# PIPELINE.add_delete_unlinked_patterns()
PIPELINE.delete_spacy_ents()
PIPELINE.delete_partial_traits(partial_traits=PARTIAL_TRAITS)

# for name in PIPELINE.nlp.pipe_names:
#     print(name)


def test(text: str) -> list[dict]:
    text = shorten(text)
    doc = PIPELINE(text)
    traits = [e._.data for e in doc.ents]

    # from pprint import pp
    # pp(traits, compact=True)

    return traits
