from dataclasses import dataclass

from spacy import Language
from traiter.pylib.traits.base_custom_pipe import BaseCustomPipe

PART_LOCATION_CUSTOM_PIPE = "part_location_custom_pipe"


@Language.factory(PART_LOCATION_CUSTOM_PIPE)
@dataclass()
class PartLocationPipe(BaseCustomPipe):
    replace: dict[str, str]
    labels: list[str]

    def __call__(self, doc):
        for ent in [e for e in doc.ents if e.label_ in self.labels]:
            frags = []
            for token in ent:
                frag = self.replace.get(token.lower_, token.lower_)
                frags.append(frag)
            ent._.data[ent.label_] = " ".join(frags)
        return doc
