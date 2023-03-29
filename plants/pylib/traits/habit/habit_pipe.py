from pathlib import Path

from spacy import Language
from traiter.pylib import add_pipe as add
from traiter.pylib import trait_util

HERE = Path(__file__).parent
TRAIT = HERE.stem

FUNC = f"{TRAIT}_func"
CSV = HERE / f"{TRAIT}.csv"

SHAPE_DIR = HERE.parent / "shape"
SHAPE_CSV = SHAPE_DIR / "shape.csv"


def pipe(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(
            nlp,
            name=f"{TRAIT}_lower",
            attr="lower",
            path=HERE / f"{TRAIT}_terms_lower.jsonl",
            **kwargs,
        )

    prev = add.ruler_pipe(
        nlp,
        name=f"{TRAIT}_patterns",
        path=HERE / f"{TRAIT}_patterns.jsonl",
        after=prev,
        overwrite_ents=True,
    )

    prev = add.data_pipe(nlp, FUNC, after=prev)

    prev = add.cleanup_pipe(
        nlp,
        name=f"{TRAIT}_cleanup",
        remove=trait_util.labels_to_remove(CSV, TRAIT),
        after=prev,
    )

    return prev


# ###############################################################################
REPLACE = trait_util.term_data(CSV, "replace")
REPLACE |= trait_util.term_data(SHAPE_CSV, "replace")


@Language.component(FUNC)
def data_func(doc):
    for ent in [e for e in doc.ents if e.label_ == TRAIT]:
        frags = [REPLACE.get(t.lower_, t.lower_) for t in ent]
        ent._.data["habit"] = " ".join(frags)
    return doc
