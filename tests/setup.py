from traiter.pylib.util import shorten

from plants.pylib import pipeline

# from plants.pylib import const

PIPELINE = pipeline.build()
# PIPELINE = pipeline.build(MODEL_PATH)
# PIPELINE = pipeline.load(MODEL_PATH)


def test(text: str) -> list[dict]:
    text = shorten(text)
    doc = PIPELINE(text)
    traits = [e._.data for e in doc.ents]

    from pprint import pp

    pp(traits, compact=True)

    return traits
