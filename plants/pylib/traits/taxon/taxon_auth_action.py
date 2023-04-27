from spacy import registry
from traiter.pylib import const as t_const

from .taxon_action import AND

TAXON_AUTH_MATCH = "taxon_auth_match"
TAXON_LINNAEUS_MATCH = "taxon_linnaeus_match"
TAXON_NOT_LINNAEUS_MATCH = "taxon_not_linnaeus_match"


@registry.misc(TAXON_AUTH_MATCH)
def taxon_auth_match(ent):
    auth = []
    data = {}

    for token in ent:

        if token._.flag == "taxon_data":
            data = token._.data

        elif token._.flag == "taxon":
            pass

        elif auth and token.lower_ in AND:
            auth.append("and")

        elif token.shape_ in t_const.NAME_SHAPES:
            if len(token) == 1:
                auth.append(token.text + ".")
            else:
                auth.append(token.text)

        token._.flag = "taxon"

    ent._.data = data

    ent._.data["authority"] = " ".join(auth)

    ent[0]._.data = ent._.data
    ent[0]._.flag = "taxon_data"


@registry.misc(TAXON_LINNAEUS_MATCH)
def taxon_linnaeus_match(ent):
    for token in ent:

        if token._.flag == "taxon_data":
            ent._.data = token._.data

        token._.flag = "taxon"

    ent._.data["authority"] = "Linnaeus"

    ent[0]._.data = ent._.data
    ent[0]._.flag = "taxon_data"


@registry.misc(TAXON_NOT_LINNAEUS_MATCH)
def taxon_not_linnaeus_match(ent):
    auth = []
    for token in ent:

        if token._.flag == "taxon_data":
            ent._.data = token._.data

        elif token.shape_ in t_const.NAME_SHAPES:
            if len(token) == 1:
                auth.append(token.text + ".")
            else:
                auth.append(token.text)

        token._.flag = "taxon"

    ent._.data["authority"] = " ".join(auth)

    ent[0]._.data = ent._.data
    ent[0]._.flag = "taxon_data"
