#!/usr/bin/env python3
import logging
import sqlite3
from collections import defaultdict

from pylib import const
from pylib import taxon_utils as tu
from tqdm import tqdm
from traiter.pylib import log


class Taxon:
    def __init__(self, **kwargs):
        self.term_set = kwargs["term_set"]
        self.label = kwargs["label"]
        self.pattern = kwargs["pattern"]
        self.attr = kwargs["attr"]
        self.replace = kwargs["replace"]
        self.rank = kwargs["extra1"]
        self.options = kwargs["extra2"].split(",")


def main():
    log.started()
    args = tu.parse_args()
    raw_taxa = tu.get_raw_taxa(args)

    rank_utils: tu.Ranks = tu.Ranks()
    taxa: list[Taxon] = get_taxa()
    taxon_by_rank = get_taxa_by_rank(taxa)
    audit_species(taxon_by_rank["species"])
    audit_forms(raw_taxa, rank_utils)

    log.finished()


def get_taxa():
    with sqlite3.connect(const.FULL_TAXON_DB) as cxn:
        cxn.row_factory = sqlite3.Row
        sql = """select * from terms where term_set = 'taxa'"""
        taxa = [Taxon(**t) for t in tqdm(cxn.execute(sql), desc="read taxa")]
    return taxa


def get_taxa_by_rank(taxa):
    taxa_by_rank = defaultdict(list)
    for taxon in tqdm(taxa, desc="terms"):
        taxa_by_rank[taxon.rank].append(taxon)

    for rank, terms in taxa_by_rank.items():
        logging.info(f"{rank:15} {len(terms)}")

    return taxa_by_rank


def audit_species(species):
    logging.info("Auditing species")
    for taxon in species:
        wc = len(taxon.pattern.split())
        if wc != 2:
            logging.error(taxon.pattern)


def audit_forms(raw_taxa, rank_utils):
    logging.info("Auditing taxon forms")
    patterns = defaultdict(int)
    for taxon, ranks in tqdm(raw_taxa.items(), desc="forms"):
        words = taxon.split()
        keys = []
        for word in words:
            if word in rank_utils.all_ranks:
                keys.append(rank_utils.pattern2rank[word])
            else:
                keys.append("x---x")
        pattern = " ".join(keys)
        patterns[pattern] += 1

    for pattern, count in sorted(patterns.items()):
        logging.info(f"{count: 8} {pattern}")


if __name__ == "__main__":
    main()
