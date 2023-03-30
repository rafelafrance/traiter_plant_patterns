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

    prev = add.ruler_pipe(
        nlp,
        name=f"{TRAIT}_patterns",
        path=HERE / f"{TRAIT}_patterns.jsonl",
        after=prev,
        overwrite_ents=True,
    )

    # from traiter.pylib.pipes import debug
    # prev = debug.tokens(nlp, after=prev)

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


@Language.component(FUNC)
def data_func(doc):
    for ent in [e for e in doc.ents if e.label_ == TRAIT]:
        surface = {}  # Dicts preserve order sets do not
        for token in ent:
            if token._.term == "surface_term" and token.text != "-":
                word = REPLACE.get(token.lower_, token.lower_)
                surface[word] = 1
        surface = " ".join(surface)
        surface = REPLACE.get(surface, surface)
        ent._.data[TRAIT] = surface

    return doc
