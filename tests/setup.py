from traiter.pylib.util import shorten

from plants.pylib.pipeline import pipeline

PIPELINE = pipeline()


def test(text: str) -> list[dict]:
    text = shorten(text)
    doc = PIPELINE(text)
    traits = [e._.data for e in doc.ents]

    from pprint import pp

    pp(traits, compact=True)

    return traits
