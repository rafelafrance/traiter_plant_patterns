import spacy
from traiter.pylib import tokenizer
from traiter.pylib.pipes import debug  # #########################
from traiter.pylib.pipes import extensions

from .traits.delete_missing import delete_missing_pipeline
from .traits.habit import habit_pipeline
from .traits.link_location import link_location_pipeline
from .traits.link_part import link_part_pipeline
from .traits.link_sex import link_sex_pipeline
from .traits.link_taxon_like import link_taxon_like_pipeline
from .traits.margin import margin_pipeline
from .traits.misc import misc_pipeline
from .traits.numeric import numeric_pipeline
from .traits.part import part_pipeline
from .traits.part_location import part_location_pipeline
from .traits.shape import shape_pipeline
from .traits.surface import surface_pipeline
from .traits.taxon import taxon_pipeline
from .traits.taxon_like import taxon_like_pipeline

# debug.tokens(nlp)  # #############################################


def build(model_path=None):
    extensions.add_extensions()

    nlp = spacy.load("en_core_web_sm", exclude=["parser", "ner"])

    tokenizer.setup_tokenizer(nlp)

    taxon_pipeline.build(nlp, extend=2)

    misc_pipeline.build(nlp)
    part_pipeline.build(nlp)

    numeric_pipeline.build(nlp)

    habit_pipeline.build(nlp)
    margin_pipeline.build(nlp)
    shape_pipeline.build(nlp)
    surface_pipeline.build(nlp)

    part_location_pipeline.build(nlp)
    taxon_like_pipeline.build(nlp)

    link_part_pipeline.build(nlp)
    link_sex_pipeline.build(nlp)
    link_location_pipeline.build(nlp)
    link_taxon_like_pipeline.build(nlp)

    delete_missing_pipeline.build(nlp)

    if model_path:
        nlp.to_disk(model_path)

    # for name in nlp.pipe_names:
    #     print(name)

    return nlp


def load(model_path):
    extensions.add_extensions()
    nlp = spacy.load(model_path)
    return nlp
