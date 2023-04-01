import re
from dataclasses import dataclass

from spacy import Language
from traiter.pylib.traits.base_custom_pipe import BaseCustomPipe

CUSTOM_PIPE = "shape_custom_pipe"


@Language.factory(CUSTOM_PIPE)
@dataclass()
class ShapePipe(BaseCustomPipe):
    trait: str
    replace: dict[str, str]

    def __call__(self, doc):
        for ent in [e for e in doc.ents if e.label_ == self.trait]:

            # Handle 3-angular etc.
            if re.match(r"^\d", ent.text):
                ent._.data[self.trait] = "polygonal"

            # All other shapes
            else:
                shape = {}  # Dicts preserve order sets do not
                for token in ent:
                    if token._.term == "shape_term" and token.text != "-":
                        word = self.replace.get(token.lower_, token.lower_)
                        shape[word] = 1
                shape = "-".join(shape)
                shape = self.replace.get(shape, shape)
                ent._.data[self.trait] = shape

        return doc
