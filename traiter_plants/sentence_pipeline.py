from spacy.lang.en import English
from traiter.pipes.sentence_pipe import SENTENCE

from . import tokenizer


def pipeline():
    nlp = English()
    tokenizer.setup_tokenizer(nlp)
    nlp.add_pipe(SENTENCE, config={"abbrev": tokenizer.ABBREVS})
    return nlp
