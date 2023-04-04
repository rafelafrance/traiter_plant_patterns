from dataclasses import dataclass

from spacy import Language
from traiter.pylib.traits.base_custom_pipe import BaseCustomPipe

HABIT_CUSTOM_PIPE = "habit_custom_pipe"


@Language.factory(HABIT_CUSTOM_PIPE)
@dataclass()
class HabitPipe(BaseCustomPipe):
    replace: dict[str, str]

    def __call__(self, doc):
        for ent in [e for e in doc.ents if e.label_ == "habit"]:
            frags = [self.replace.get(t.lower_, t.lower_) for t in ent]
            ent._.data["habit"] = " ".join(frags)
        return doc
