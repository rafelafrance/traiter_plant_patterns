import re
from dataclasses import dataclass

from spacy import Language
from traiter.pylib.traits.base_custom_pipe import BaseCustomPipe

PART_CUSTOM_PIPE = "part_custom_pipe"


@Language.factory(PART_CUSTOM_PIPE)
@dataclass()
class PartPipe(BaseCustomPipe):
    replace: dict[str, str]
    labels: list[str]

    def __call__(self, doc):
        for ent in [e for e in doc.ents if e.label_ in self.labels]:
            frags = [[]]
            label = ent.label_

            for token in ent:
                token._.flag = "part"

                if token._.term in self.labels:
                    part = self.replace.get(token.lower_, token.lower_)
                    if part not in frags[-1]:
                        frags[-1].append(part)
                    if label not in ("missing_part", "multiple_parts", "subpart"):
                        label = token._.term

                elif token._.term == "missing":
                    frags[-1].append(self.replace.get(token.lower_, token.lower_))

                elif token._.term == "part_and":
                    frags.append([])

            all_parts = [" ".join(f) for f in frags]
            all_parts = [re.sub(r" - ", "-", p) for p in all_parts]
            all_parts = [self.replace.get(p, p) for p in all_parts]

            ent._.data["trait"] = label
            ent._.data[label] = all_parts[0] if len(all_parts) == 1 else all_parts

            ent[0]._.data = ent._.data  # Cache so we can use this in counts

        return doc
