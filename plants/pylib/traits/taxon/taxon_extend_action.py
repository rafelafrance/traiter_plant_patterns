from spacy import registry
from traiter.pylib import const as t_const

from .taxon_action import AND
from .taxon_action import LOWER_RANK
from .taxon_action import MAYBE
from .taxon_action import RANK_ABBREV
from .taxon_action import RANK_REPLACE

TAXON_EXTEND_MATCH = "taxon_extend_match"


@registry.misc(TAXON_EXTEND_MATCH)
def taxon_extend_match(ent):
    auth = []
    taxon = []
    rank = ""
    next_is_lower_taxon = False

    for token in ent:

        if token._.flag == "taxon_data":
            ent._.data = token._.data
            taxon.append(ent._.data["taxon"])
            if ent._.data.get("authority"):
                auth.append(ent._.data["authority"])

        elif token._.flag == "taxon" or token.text in "().":
            pass

        elif auth and token.lower_ in AND:
            auth.append("and")

        elif token.shape_ in t_const.NAME_SHAPES:
            if len(token) == 1:
                auth.append(token.text + ".")
            else:
                auth.append(token.text)

        elif token._.term in LOWER_RANK:
            taxon.append(RANK_ABBREV.get(token.lower_, token.lower_))
            rank = RANK_REPLACE.get(token.lower_, token.text)
            next_is_lower_taxon = True

        elif next_is_lower_taxon:
            taxon.append(token.lower_)
            next_is_lower_taxon = False

        token._.flag = "taxon"

    ent._.data["taxon"] = " ".join(taxon)
    ent._.data["rank"] = rank
    ent._.data["authority"] = auth
    ent._.relabel = "taxon"

    ent[0]._.data = ent._.data
    ent[0]._.flag = "taxon_data"
