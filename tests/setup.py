from traiter.pylib.util import shorten

from plants.pylib.pipeline_builder import PipelineBuilder

PIPELINE = PipelineBuilder(exclude="ner")
PIPELINE.tokenizer()
PIPELINE.taxon_terms()
PIPELINE.taxa()
PIPELINE.taxa_plus(n=2)
PIPELINE.plant_terms()
PIPELINE.parts()
PIPELINE.sex()
# PIPELINE.debug_tokens()  # ####################################
PIPELINE.numerics()
PIPELINE.shapes()
PIPELINE.margins()
PIPELINE.colors()
PIPELINE.part_locations()
PIPELINE.taxa_like()
PIPELINE.delete_partial_traits()
PIPELINE.link_parts()
PIPELINE.link_parts_once()
PIPELINE.link_subparts()
PIPELINE.link_subparts_suffixes()
PIPELINE.link_sex()
PIPELINE.link_locations()
PIPELINE.link_taxa_like()
PIPELINE.delete_unlinked()
PIPELINE.delete_spacy_ents()
PIPELINE.delete_partial_traits(name="final_deletes")
# PIPELINE.debug_ents()  # ####################################

# for name in PIPELINE.nlp.pipe_names:
#     print(name)


def test(text: str) -> list[dict]:
    text = shorten(text)
    doc = PIPELINE(text)
    traits = [e._.data for e in doc.ents]

    # from pprint import pp
    # pp(traits, compact=True)

    return traits
