import re
from dataclasses import dataclass

from spacy import Language
from traiter.pylib.traits.base_custom_pipe import BaseCustomPipe

CUSTOM_PIPE_RANGE = "custom_pipe_range"


@Language.factory(CUSTOM_PIPE_RANGE)
@dataclass()
class RangePipe(BaseCustomPipe):
    def __call__(self, doc):
        for ent in [e for e in doc.ents if e.label_ == "range"]:
            nums = []
            for token in ent:
                token._.flag = "range"
                nums += re.findall(r"\d*\.?\d+", token.text)

            # Cache the values in the first token
            keys = ent.id_.split(".")[1:]
            ent[0]._.data = {k: v for k, v in zip(keys, nums)}

        return doc
