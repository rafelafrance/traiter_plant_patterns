from pathlib import Path

from spacy import Language
from traiter.pylib import add_pipe as add
from traiter.pylib import trait_util

from .part_compilers import PART_LABELS

HERE = Path(__file__).parent
TRAIT = HERE.stem

FUNC = f"{TRAIT}_func"
CSV = HERE / f"{TRAIT}.csv"

LABELS = PART_LABELS + "missing_part missing_subpart multiple_parts subpart".split()


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
        frags = [[]]
        for token in ent:
            if token._.term in LABELS:
                frags[-1].append(REPLACE.get(token.lower_, token.lower_))
            elif token._.term == "part_missing":
                frags[-1].append(REPLACE.get(token.lower_, token.lower_))
            elif token._.term == "part_and":
                frags.append([])
        all_parts = [" ".join(f) for f in frags]
        ent._.data[ent.label_] = all_parts[0] if len(all_parts) == 1 else all_parts
    return doc
