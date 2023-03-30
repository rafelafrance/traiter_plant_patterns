from pathlib import Path

from spacy import Language
from traiter.pylib import add_pipe as add
from traiter.pylib import trait_util

HERE = Path(__file__).parent
TRAIT = HERE.stem

FUNC = f"{TRAIT}_func"
CSV = HERE / f"{TRAIT}.csv"

LABELS = trait_util.get_labels(CSV)


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
        remove=trait_util.labels_to_remove(CSV, LABELS),
        after=prev,
    )

    return prev


# ###############################################################################
REPLACE = trait_util.term_data(CSV, "replace")


@Language.component(FUNC)
def data_func(doc):
    for ent in [e for e in doc.ents if e.label_ in LABELS]:
        frags = []
        for token in ent:
            frag = REPLACE.get(token.lower_, token.lower_)
            if token._.term == "joined":
                ent._.data["joined"] = frag
            else:
                frags.append(frag)
        ent._.data[ent.label_] = " ".join(frags)
    return doc
