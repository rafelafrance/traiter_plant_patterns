from dataclasses import dataclass

from spacy import Language
from traiter.pylib.traits.base_custom_pipe import BaseCustomPipe

CUSTOM_PIPE = "margin_custom_pipe"


@Language.factory(CUSTOM_PIPE)
@dataclass()
class HabitatPipe(BaseCustomPipe):
    trait: str
    replace: dict[str, str]

    def __call__(self, doc):
        for ent in [e for e in doc.ents if e.label_ == self.trait]:
            margin = {}  # Dicts preserve order sets do not
            for token in ent:
                if token._.term in ["margin", "shape"] and token.text != "-":
                    word = self.replace.get(token.lower_, token.lower_)
                    margin[word] = 1
            margin = "-".join(margin)
            margin = self.replace.get(margin, margin)
            ent._.data[self.trait] = margin

        return doc
