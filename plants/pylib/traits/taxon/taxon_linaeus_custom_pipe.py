from dataclasses import dataclass

from spacy import Language
from traiter.pylib.traits.base_custom_pipe import BaseCustomPipe

TAXON_LINNAEUS_CUSTOM_PIPE = "taxon_linnaeus_auth"


@Language.factory(TAXON_LINNAEUS_CUSTOM_PIPE)
@dataclass()
class TaxonLinnaeusPipe(BaseCustomPipe):
    def __call__(self, doc):
        for ent in [e for e in doc.ents if e.label_ == "linnaeus"]:
            data = {}

            for token in ent:
                token._.flag = "linnaeus"

                if token._.data:
                    data = token._.data

            ent._.data = data
            ent._.data["authority"] = "Linnaeus"
            ent[0]._.data = ent._.data
            print(ent._.data)

        return doc
