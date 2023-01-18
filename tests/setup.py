from typing import Dict
from typing import List

from mimosa.pylib import mimosa_pipeline
from mimosa.pylib import sentence_pipeline
from traiter.util import shorten

NLP = mimosa_pipeline.pipeline()  # Singleton for testing
SENT_NLP = sentence_pipeline.pipeline()  # Singleton for testing


def test(text: str) -> List[Dict]:
    text = shorten(text)
    sent_doc = SENT_NLP(text)

    traits = []

    for sent in sent_doc.sents:
        doc = NLP(sent.text)
        for ent in doc.ents:
            trait = ent._.data
            trait["start"] += sent.start_char
            trait["end"] += sent.start_char
            traits.append(trait)

    # from pprint import pp
    # pp(traits, compact=True)

    return traits
