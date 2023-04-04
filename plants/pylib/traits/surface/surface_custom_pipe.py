from dataclasses import dataclass

from spacy import Language
from traiter.pylib.traits.base_custom_pipe import BaseCustomPipe

SURFACE_CUSTOM_PIPE = "surface_custom_pipe"


@Language.factory(SURFACE_CUSTOM_PIPE)
@dataclass()
class ShapePipe(BaseCustomPipe):
    replace: dict[str, str]

    def __call__(self, doc):
        for ent in [e for e in doc.ents if e.label_ == "surface"]:
            surface = {}  # Dicts preserve order sets do not
            for token in ent:
                if token._.term == "surface_term" and token.text != "-":
                    word = self.replace.get(token.lower_, token.lower_)
                    surface[word] = 1
            surface = " ".join(surface)
            surface = self.replace.get(surface, surface)
            ent._.data["surface"] = surface

        return doc
