from dataclasses import dataclass

from spacy import Language
from traiter.pylib import util as t_util
from traiter.pylib.traits.base_custom_pipe import BaseCustomPipe

CUSTOM_PIPE_COUNT = "custom_pipe_count"


@Language.factory(CUSTOM_PIPE_COUNT)
@dataclass()
class CountPipe(BaseCustomPipe):
    trait: str
    replace: dict[str, str]

    def __call__(self, doc):
        for ent in [e for e in doc.ents if e.label_ == self.trait]:

            if ent.id_ == "count_word":
                ent._.data["low"] = int(self.replace[ent[0].lower_])

            elif ent.id_ == "count":
                per_part = []
                for token in ent:
                    if token._.data and token._.flag == "range":
                        for key, value in token._.data.items():
                            ent._.data[key] = t_util.to_positive_int(value)
                    elif token._.data and token._.flag == "part":
                        part_trait = token._.data["trait"]
                        ent._.data["per_part"] = token._.data[part_trait]
                    elif token._.term == "per_count":
                        per_part.append(token.lower_)

                if per_part:
                    per_part = " ".join(per_part)
                    ent._.data["count_group"] = self.replace.get(per_part, per_part)

        return doc
