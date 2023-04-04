from dataclasses import dataclass

from spacy import Language
from traiter.pylib.traits.base_custom_pipe import BaseCustomPipe

MARGIN_CUSTOM_PIPE = "margin_custom_pipe"


@Language.factory(MARGIN_CUSTOM_PIPE)
@dataclass()
class HabitatPipe(BaseCustomPipe):
    replace: dict[str, str]

    def __call__(self, doc):
        for ent in [e for e in doc.ents if e.label_ == "margin"]:
            margin = {}  # Dicts preserve order sets do not
            for token in ent:
                if token._.term in ["margin", "shape"] and token.text != "-":
                    word = self.replace.get(token.lower_, token.lower_)
                    margin[word] = 1
            margin = "-".join(margin)
            margin = self.replace.get(margin, margin)
            ent._.data["margin"] = margin

        return doc
