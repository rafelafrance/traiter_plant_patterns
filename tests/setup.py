from traiter.pylib.util import shorten

from plants.pylib.patterns.delete import PARTIAL_TRAITS
from plants.pylib.pipeline_builder import PipelineBuilder

PIPELINE = PipelineBuilder()
PIPELINE.tokenizer()
PIPELINE.taxon_terms(before="ner")
# PIPELINE.debug_tokens(before="ner")  # ####################################
PIPELINE.taxa(before="ner")
PIPELINE.taxa_plus(n=2, before="ner")
PIPELINE.plant_terms(before="ner")
PIPELINE.parts(before="ner")
PIPELINE.sex(before="ner")
PIPELINE.numerics(before="ner")
PIPELINE.part_locations(before="ner")
PIPELINE.colors(before="ner")
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
PIPELINE.delete_partial_traits(partial_traits=PARTIAL_TRAITS, name="final_deletes")

# for name in PIPELINE.nlp.pipe_names:
#     print(name)


def test(text: str) -> list[dict]:
    text = shorten(text)
    doc = PIPELINE(text)
    traits = [e._.data for e in doc.ents]

    from pprint import pp

    pp(traits, compact=True)

    return traits
