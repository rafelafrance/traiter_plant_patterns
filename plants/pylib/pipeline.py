import spacy
from traiter.pylib import tokenizer
from traiter.pylib.pipes import extensions
from traiter.pylib.pipes.finish import FINSH

from .traits.basic import basic_pipe
from .traits.habit import habit_pipe
from .traits.link_location import link_location_pipe
from .traits.link_part import link_part_pipe
from .traits.link_sex import link_sex_pipe
from .traits.part import part_pipe
from .traits.part_location import part_location_pipe
from .traits.shape import shape_pipe
from .traits.surface import surface_pipe


def pipeline():
    extensions.add_extensions()

    nlp = spacy.load("en_core_web_sm", exclude=["ner", "parser"])

    tokenizer.setup_tokenizer(nlp)

    basic_pipe.pipe(nlp)
    habit_pipe.pipe(nlp)

    # pipes.taxon_terms()
    # pipes.taxa(n=2)
    # pipes.taxa_like()

    part_pipe.pipe(nlp)
    # pipes.numerics()
    shape_pipe.pipe(nlp)
    surface_pipe.pipe(nlp)
    # pipes.margins()
    # pipes.colors()
    part_location_pipe.pipe(nlp)

    nlp.add_pipe(FINSH)

    link_part_pipe.pipe(nlp)
    link_sex_pipe.pipe(nlp)
    link_location_pipe.pipe(nlp)
    # pipes.link_taxa_like()

    # from traiter.pylib.pipes import debug  # ##################
    # debug.tokens(nlp)  # ######################################

    # for name in nlp.pipe_names:
    #     print(name)

    return nlp
