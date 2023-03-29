from pathlib import Path

from spacy import Language
from traiter.pylib import add_pipe as add
from traiter.pylib import trait_util

HERE = Path(__file__).parent
TRAIT = HERE.stem

FUNC = f"{TRAIT}_func"
CSV = HERE / f"{TRAIT}.csv"


def pipe(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(
            nlp,
            name=f"{TRAIT}_lower",
            attr="lower",
            path=HERE / f"{TRAIT}_terms_lower.jsonl",
            **kwargs,
        )

    prev = add.data_pipe(nlp, FUNC, after=prev)

    return prev


# ###############################################################################
REPLACE = trait_util.term_data(CSV, "replace")
LABELS = trait_util.get_labels(CSV)


@Language.component(FUNC)
def data_func(doc):
    for ent in [e for e in doc.ents if e.label_ in LABELS]:
        frags = [REPLACE.get(t.lower_, t.lower_) for t in ent]
        ent._.data[ent.label_] = " ".join(frags)
    return doc
