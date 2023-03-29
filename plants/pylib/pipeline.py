import spacy
from traiter.pylib import tokenizer
from traiter.pylib.pipes import extensions
from traiter.pylib.pipes.finish import FINSH

from .traits.basic import basic_pipe
from .traits.habit import habit_pipe
from .traits.link_part import link_part_pipe
from .traits.part import part_pipe

# from traiter.pylib.pipes import debug


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
    # pipes.sex()
    # pipes.numerics()
    # pipes.shapes()
    # pipes.margins()
    # pipes.colors()
    # pipes.part_location()

    link_part_pipe.pipe(nlp)
    # pipes.link_sex()
    # pipes.link_locations()
    # pipes.link_taxa_like()

    nlp.add_pipe(FINSH)

    # debug.tokens(nlp)  # ####################################

    # for name in nlp.pipe_names:
    #     print(name)

    return nlp
