from .patterns import deletes
from .pipeline_builder import PipelineBuilder
from .vocabulary import terms


def pipeline():
    pipes = PipelineBuilder(exclude="ner")

    pipes.traits_without_matcher = terms.TRAITS_WITHOUT_MATCHER

    pipes.tokenizer()

    pipes.taxon_terms()
    pipes.taxa(n=2)
    pipes.taxa_like()

    pipes.plant_terms()
    pipes.parts()
    pipes.sex()
    pipes.numerics()
    pipes.shapes()
    pipes.margins()
    pipes.colors()
    pipes.part_location()

    pipes.delete_traits("delete_partials", keep_outputs=True)

    pipes.link_parts()
    pipes.link_parts_once()
    pipes.link_subparts()
    pipes.link_subparts_suffixes()
    pipes.link_sex()
    pipes.link_locations()
    pipes.link_taxa_like()

    pipes.delete_traits("final_delete", delete_when=deletes.DELETE_WHEN)

    # pipes.debug_tokens()  # ####################################

    return pipes.build()
