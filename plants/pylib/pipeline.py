import spacy
from traiter.pylib import tokenizer
from traiter.pylib.pipes import extensions
from traiter.pylib.pipes.finish import FINSH

from .traits.habit import habit_pipeline
from .traits.link_location import link_location_pipeline
from .traits.link_part import link_part_pipeline
from .traits.link_sex import link_sex_pipeline
from .traits.margin import margin_pipeline
from .traits.misc import misc_pipeline
from .traits.numeric import numeric_pipeline
from .traits.part import part_pipeline
from .traits.part_location import part_location_pipeline
from .traits.shape import shape_pipeline
from .traits.surface import surface_pipeline
from .traits.taxon import taxon_pipeline

# from traiter.pylib.pipes import debug  # #########################
# debug.tokens(nlp)  # #############################################


def build(model_path=None):
    extensions.add_extensions()

    nlp = spacy.load("en_core_web_sm", exclude=["ner", "parser"])

    tokenizer.setup_tokenizer(nlp)

    taxon_pipeline.build(nlp)
    # pipes.taxa(n=2)
    # pipes.taxa_like()

    part_pipeline.build(nlp)
    numeric_pipeline.build(nlp)

    habit_pipeline.build(nlp)
    margin_pipeline.build(nlp)
    shape_pipeline.build(nlp)
    surface_pipeline.build(nlp)

    misc_pipeline.build(nlp)

    part_location_pipeline.build(nlp)

    nlp.add_pipe(FINSH)

    link_part_pipeline.build(nlp)
    link_sex_pipeline.build(nlp)
    link_location_pipeline.build(nlp)
    # pipes.link_taxa_like()

    if model_path:
        nlp.to_disk(model_path)

    return nlp


def load(model_path):
    extensions.add_extensions()
    nlp = spacy.load(model_path)
    return nlp
