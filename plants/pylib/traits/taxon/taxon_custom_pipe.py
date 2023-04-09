import re
from dataclasses import dataclass

from spacy import Language
from traiter.pylib import const as t_const
from traiter.pylib.traits.base_custom_pipe import BaseCustomPipe

from ... import const
from .taxon_patterns import ABBREV_RE

TAXON_CUSTOM_PIPE = "taxon_custom_pipe"


@Language.factory(TAXON_CUSTOM_PIPE)
@dataclass()
class TaxonPipe(BaseCustomPipe):
    level: dict[str, str]
    rank_replace: dict[str, str]
    rank_abbrev: dict[str, str]
    monomial_ranks: dict[str, str]
    binomial_abbrev: dict[str, str]

    def __call__(self, doc):
        for ent in [e for e in doc.ents if e.label_ == "taxon"]:
            if ent.id_ == "singleton":
                self.on_single_taxon_match(ent)
            else:
                self.on_taxon_match(ent)
        return doc

    def on_single_taxon_match(self, ent):
        rank = None
        taxon = None

        for token in ent:
            token._.flag = "taxon"

            # Taxon and its rank
            if token._.term == "monomial":
                taxon = token.lower_
                taxon = taxon.replace("- ", "-")

                # A given rank will override the one in the DB
                rank_ = self.monomial_ranks.get(token.lower_)
                if not rank and rank_:
                    rank_ = rank_.split()[0]
                    level = self.level[rank_]
                    if level == "higher" and token.shape_ in t_const.NAME_SHAPES:
                        rank = rank_
                    elif (
                        level in ["lower", "species"]
                        and token.shape_ not in t_const.TITLE_SHAPES
                    ):
                        rank = rank_

            # A given rank overrides the one in the DB
            elif self.level.get(token.lower_) == "higher":
                rank = self.rank_replace.get(token.lower_, token.lower_)

            elif token.pos_ in ["PROPN", "NOUN"]:
                taxon = token.lower_

        if not rank:
            ent._.delete = True
            return

        taxon = taxon.title() if self.level[rank] == "higher" else taxon.lower()
        if len(taxon) < const.MIN_TAXON_LEN:
            ent._.delete = True

        ent._.data = {
            "taxon": taxon.title() if self.level[rank] == "higher" else taxon.lower(),
            "rank": rank,
        }
        ent[0]._.data = ent._.data

    def on_taxon_match(self, ent):
        taxon = []
        rank_seen = False

        for i, token in enumerate(ent):
            token._.flag = "taxon"

            if self.level.get(token.lower_) == "lower":
                taxon.append(self.rank_abbrev.get(token.lower_, token.lower_))
                rank_seen = True

            elif token._.term == "binomial" and i == 0:
                taxon.append(token.text.title())

            elif token._.term == "binomial" and i > 0:
                taxon.append(token.lower_)

            elif token._.term == "monomial" and i != 2:
                taxon.append(token.lower_)

            elif token._.term == "monomial" and i == 2:
                if not rank_seen:
                    taxon.append(self.rank_abbrev["subspecies"])
                taxon.append(token.lower_)

            elif token.pos_ in ["PROPN", "NOUN"]:
                taxon.append(token.text)

            else:
                ent._.delete = True
                return

        if re.match(ABBREV_RE, taxon[0]) and len(taxon) > 1:
            taxon[0] = taxon[0] if taxon[0][-1] == "." else taxon[0] + "."
            abbrev = " ".join(taxon[:2])
            taxon[0] = self.binomial_abbrev.get(abbrev, taxon[0])

        taxon = " ".join(taxon)
        taxon = taxon[0].upper() + taxon[1:]

        ent._.data = {"taxon": taxon, "rank": ent.id_}
        ent[0]._.data = ent._.data
