from dataclasses import dataclass
from pathlib import Path

from spacy import Language
from traiter.pylib.traits import add_pipe as add
from traiter.pylib.traits import trait_util
from traiter.pylib.traits.base_custom_pipe import BaseCustomPipe

from .pattern_compilers import COMPILERS

HERE = Path(__file__).parent
TRAIT = HERE.stem

CUSTOM_PIPE = "surface_custom_pipe"
CSV = HERE / f"{TRAIT}.csv"


def build(nlp: Language, **kwargs):
    with nlp.select_pipes(enable="tokenizer"):
        prev = add.term_pipe(nlp, name=f"{TRAIT}_terms", path=CSV, **kwargs)

    prev = add.ruler_pipe(
        nlp,
        name=f"{TRAIT}_patterns",
        compiler=COMPILERS,
        after=prev,
        overwrite_ents=True,
    )

    config = {
        "trait": TRAIT,
        "replace": trait_util.term_data(CSV, "replace"),
    }
    prev = add.custom_pipe(nlp, CUSTOM_PIPE, config=config, after=prev)

    prev = add.cleanup_pipe(
        nlp,
        name=f"{TRAIT}_cleanup",
        remove=trait_util.labels_to_remove(CSV, keep=TRAIT),
        after=prev,
    )

    return prev


@Language.factory(CUSTOM_PIPE)
@dataclass()
class ShapePipe(BaseCustomPipe):
    trait: str
    replace: dict[str, str]

    def __call__(self, doc):
        for ent in [e for e in doc.ents if e.label_ == self.trait]:
            surface = {}  # Dicts preserve order sets do not
            for token in ent:
                if token._.term == "surface_term" and token.text != "-":
                    word = self.replace.get(token.lower_, token.lower_)
                    surface[word] = 1
            surface = " ".join(surface)
            surface = self.replace.get(surface, surface)
            ent._.data[self.trait] = surface

        return doc
