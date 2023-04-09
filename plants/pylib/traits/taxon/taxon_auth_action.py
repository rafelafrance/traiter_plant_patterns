from dataclasses import dataclass

from spacy import Language
from traiter.pylib import const as t_const
from traiter.pylib.traits.base_custom_pipe import BaseCustomPipe

from .taxon_auth_patterns import AND

TAXON_AUTH_CUSTOM_PIPE = "taxon_auth"


@Language.factory(TAXON_AUTH_CUSTOM_PIPE)
@dataclass()
class TaxonAuthPipe(BaseCustomPipe):
    def __call__(self, doc):
        for ent in [e for e in doc.ents if e.label_ in ("taxon", "is_auth")]:
            print(ent)
            auth = []
            data = {}

            for token in ent:

                if token._.data:
                    data = token._.data

                elif token._.flag == "taxon":
                    pass

                elif auth and token.lower_ in AND:
                    auth.append("and")

                elif token._.flag != "taxon" and token.shape_ in t_const.NAME_SHAPES:
                    if len(token) == 1:
                        auth.append(token.text + ".")
                    else:
                        auth.append(token.text)

            ent._.data = data

            if auth and not ent._.data.get("authority"):
                auth = " ".join(auth)
                ent._.data["authority"] = auth

            ent[0]._.data = ent._.data

        return doc
