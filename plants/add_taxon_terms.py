#!/usr/bin/env python3
"""Use binomial species names but single taxon names for higher and lower ranks."""
import argparse
import csv
import logging
import sqlite3
import sys
import textwrap
import zipfile
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import regex
from pylib.vocabulary import terms
from tqdm import tqdm
from traiter.pylib import log
from traiter.pylib.term_list import TermList

ITIS_SPECIES_ID = 220


@dataclass
class Record:
    label: str
    pattern: str
    ranks: str


class Ranks:
    def __init__(self):
        self.ranks = TermList().read(terms.VOCAB_DIR / "ranks.csv")
        self.id2rank = {int(r["rank_id"]): r["replace"] for r in self.ranks}
        self.rank_names = {r["pattern"]: r["replace"] for r in self.ranks}
        self.lower = {r for i, r in self.id2rank.items() if i > ITIS_SPECIES_ID}
        self.higher = {r for i, r in self.id2rank.items() if i < ITIS_SPECIES_ID}

    def normalize_rank(self, rank):
        rank = rank.lower()
        return self.rank_names.get(rank, "")


class Taxa:
    def __init__(self, ranks):
        self.ranks = ranks
        self.taxon = defaultdict(set)  # Ranks for each term
        self.valid_pattern = regex.compile(r"^\p{L}[\p{L}\s'.-]*\p{L}$")

    def add_taxon_and_rank(self, pattern, rank):
        words = pattern.split()

        if rank not in self.ranks.rank_names:
            return

        if len(words) == 1:
            self.taxon[pattern.lower()].add(rank)

        elif len(words) >= 2:
            self.add_binomial(words)
            rank = rank
            for word in words[2:]:
                if new_rank := self.ranks.rank_names.get(word):
                    rank = new_rank
                else:
                    self.taxon[word.lower()].add(rank)

    def add_binomial(self, words):
        binomial = f"{words[0].title()} {words[1].lower()}"
        genus = words[0].lower()
        species = words[1].lower()
        self.taxon[binomial].add("species")
        self.taxon[genus].add("genus")
        self.taxon[species].add("species")

    def add_taxa_and_ranks(self, pattern, ranks):
        for rank in ranks:
            self.add_taxon_and_rank(pattern, rank)

    def remove_problem_taxa(self, show_rejected):
        """Some taxa interfere with other parses."""
        new = {}

        problem_words = {"temp", "uncertain", "unknown", "dummy", "name"}

        problem_taxa = {"harms", "side", "may", "lake"}
        problem_taxa |= {t["pattern"].lower() for t in terms.PLANT_TERMS}
        shared = "colors habitats us_locations"
        problem_taxa |= {t["pattern"].lower() for t in TermList().shared(shared)}

        taxa = sorted(self.taxon.items())

        for taxon, rank in taxa:
            words = taxon.split()

            if taxon.lower() in problem_taxa:
                print(f"Removed {taxon} {rank}")
                continue

            if any(w.lower() in problem_words for w in words):
                print(f"Removed {taxon} {rank}")
                continue

            if not self.valid_pattern.match(taxon):
                if show_rejected:
                    print(f"Removed {taxon} {rank}")
                continue

            if len(taxon) < terms.MIN_TAXON_LEN:
                if show_rejected:
                    print(f"Removed {taxon} {rank}")
                continue

            if any(len(w) < terms.MIN_TAXON_WORD_LEN for w in words):
                if show_rejected:
                    print(f"Removed {taxon} {rank}")
                continue

            new[taxon] = rank

        self.taxon = new


def main():
    log.started()

    ranks = Ranks()
    taxa = Taxa(ranks)

    args = parse_args()

    read_taxa(args, taxa)

    taxa.remove_problem_taxa(args.show_rejected)

    records = build_records(taxa)
    counts = count_ranks(records)
    sort_ranks(counts, records, taxa)

    csv_path = terms.DATA_DIR / "taxa.csv"
    terms.TAXA_VOCAB.unlink(missing_ok=True)
    write_csv(records, csv_path)

    write_mock_csv(records)

    with zipfile.ZipFile(terms.TAXA_VOCAB, "w", zipfile.ZIP_DEFLATED) as zippy:
        zippy.write(csv_path, arcname=csv_path.name)

    log.finished()


def count_ranks(records):
    counts = defaultdict(int)
    for record in records:
        ranks = record.ranks.split()
        for rank in ranks:
            counts[rank] += 1
    return counts


def sort_ranks(counts, records, taxa):
    logging.info("Sorting ranks")

    for record in records:
        keys = []

        for rank in record.ranks.split():
            if rank in taxa.ranks.higher:
                keys.append((1, -counts[rank], rank))
            elif rank in taxa.ranks.lower:
                keys.append((2, -counts[rank], rank))
            else:
                keys.append((3, -counts[rank], rank))

        record.ranks = " ".join([k[2] for k in sorted(keys)])


def build_records(taxa):
    logging.info("Building records")

    records = []

    for taxon, ranks in taxa.taxon.items():
        word_count = len(taxon.split())
        if word_count < 3:
            records.append(
                Record(
                    label="monomial" if word_count == 1 else "binomial",
                    pattern=taxon.lower(),
                    ranks=" ".join(ranks),
                )
            )
        else:
            logging.error(f"Parse error: {taxon}")
            sys.exit(1)

    return records


def write_csv(rows, path):
    with open(path, "w") as out_csv:
        writer = csv.writer(out_csv)
        writer.writerow(""" label pattern ranks """.split())
        for r in rows:
            writer.writerow([r.label, r.pattern, r.ranks])


def write_mock_csv(records):
    mock_path = terms.VOCAB_DIR / "mock_taxa.csv"

    with open(mock_path) as in_csv:
        reader = csv.DictReader(in_csv)
        old = {r["pattern"] for r in reader}

    new = [r for r in records if r.pattern in old]
    new = sorted(new, key=lambda n: (n.label, n.pattern))

    write_csv(new, mock_path)


def read_taxa(args, taxa):
    if args.itis_db:
        read_itis_taxa(args.itis_db, taxa)

    if args.wcvp_file:
        read_wcvp_taxa(args.wcvp_file, taxa)

    if args.wfot_tsv:
        read_wfot_taxa(args.wfot_tsv, taxa)

    if args.old_taxa_csv:
        read_old_taxa(args.old_taxa_csv, taxa)

    if args.other_taxa_csv:
        read_other_taxa(args.other_taxa_csv, taxa)


def read_other_taxa(other_taxa_csv, taxa):
    with open(other_taxa_csv) as in_file:
        reader = csv.DictReader(in_file)
        for row in reader:
            taxa.add_taxon_and_rank(row["taxon"], row["rank"])


def read_old_taxa(old_taxa_csv, taxa):
    with open(old_taxa_csv) as in_file:
        reader = csv.DictReader(in_file)
        for row in list(reader):
            pattern = row["pattern"]
            ranks = set(row["ranks"].split())
            ranks -= {"species"}
            if not ranks:
                continue
            taxa.add_taxon_and_rank(pattern, ranks.pop())


def read_wfot_taxa(wfot_tsv, taxa):
    with open(wfot_tsv) as in_file:
        reader = csv.DictReader(in_file, delimiter="\t")
        for row in tqdm(reader, desc="wfot"):
            rank = taxa.ranks.normalize_rank(row["taxonRank"])
            pattern = row["scientificName"]
            taxa.add_taxon_and_rank(pattern, rank)


def read_wcvp_taxa(wcvp_file, taxa):
    with open(wcvp_file) as in_file:
        reader = csv.DictReader(in_file, delimiter="|")
        for row in tqdm(reader, desc="wcvp"):
            rank = taxa.ranks.normalize_rank(row["taxonrank"])
            pattern = row["scientfiicname"]
            taxa.add_taxon_and_rank(pattern, rank)


def read_itis_taxa(itis_db, taxa):
    itis_kingdom_id = 3

    with sqlite3.connect(itis_db) as cxn:
        cxn.row_factory = sqlite3.Row
        sql = "select complete_name, rank_id from taxonomic_units where kingdom_id = ?"
        rows = [t for t in tqdm(cxn.execute(sql, (itis_kingdom_id,)), desc="itis")]

    for row in rows:
        rank, pattern = taxa.ranks.id2rank[row["rank_id"]], row["complete_name"]
        taxa.add_taxon_and_rank(pattern, rank)


def parse_args():
    description = """Build a database taxon patterns."""
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description), fromfile_prefix_chars="@"
    )

    arg_parser.add_argument(
        "--itis-db",
        type=Path,
        metavar="PATH",
        help="""Get terms from this ITIS database.""",
    )

    arg_parser.add_argument(
        "--wcvp-file",
        type=Path,
        metavar="PATH",
        help="""Get terms from this WCVP file. It is '|' a separated CSV.""",
    )

    arg_parser.add_argument(
        "--wfot-tsv",
        type=Path,
        metavar="PATH",
        help="""Get terms from this WFO Taxonomic TSV.""",
    )

    arg_parser.add_argument(
        "--old-taxa-csv",
        type=Path,
        metavar="PATH",
        help="""Get old taxon terms from this CSV.""",
    )

    arg_parser.add_argument(
        "--other-taxa-csv",
        type=Path,
        metavar="PATH",
        help="""Get even more taxa from this CSV file.""",
    )

    arg_parser.add_argument(
        "--traiter-vocab-dir",
        type=Path,
        metavar="PATH",
        help="""We want to remove taxa that interfere with parsing standard Traiter
            terms. Enter the directory that contains the standard traiter vocabulary
            and it will scan thru this for all CSVs and remove taxa that are a direct
            match.
            """,
    )

    arg_parser.add_argument(
        "--show-rejected",
        action="store_true",
        help="""Print everything that is rejected from the CSV.""",
    )

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    main()
