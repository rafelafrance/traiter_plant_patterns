from .pipeline_builder import PipelineBuilder


def pipeline():
    pipes = PipelineBuilder(exclude="ner")

    pipes.tokenizer()

    pipes.taxon_terms()
    pipes.taxa()
    pipes.taxa_plus(n=2)
    pipes.taxa_like()

    pipes.plant_terms()
    pipes.parts()
    pipes.sex()
    pipes.numerics()
    pipes.shapes()
    pipes.margins()
    pipes.colors()
    pipes.part_locations()
    pipes.delete_partial_traits()

    pipes.link_parts()
    pipes.link_parts_once()
    pipes.link_subparts()
    pipes.link_subparts_suffixes()
    pipes.link_sex()
    pipes.link_locations()
    pipes.link_taxa_like()

    pipes.delete_unlinked()
    pipes.delete_partial_traits(name="final_deletes")

    # pipes.debug_tokens()  # ####################################

    return pipes
