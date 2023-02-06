#!/usr/bin/env python3
"""Build a database for spellchecking taxa from ITIS terms.

Based off of symmetric deletes method from SeekStorm. MIT license.
https://seekstorm.com/blog/1000x-spelling-correction/
"""
import argparse
import sqlite3
import textwrap
from pathlib import Path

from tqdm import tqdm

KINGDOM_ID = 3
SPECIES_ID = 210
SUBSPECIES_ID = 220
NOT_FOUND = 999

COLS = """
    unit_ind1 unit_name1 unit_ind2 unit_name2 unit_ind3 unit_name3 unit_ind4 unit_name4
    """.split()


def main():
    args = parse_args()

    new_taxa, ranks = get_new_taxa(args.itis_db)
    name_parts = get_taxon_name_parts(new_taxa, ranks)

    full_names = get_full_names(name_parts)
    batch = get_spell_check(full_names, args.delete_chars)

    write_database(batch, args.spell_db)


def write_database(batch, spell_db):
    insert = """
        insert into misspellings
               ( term,  miss,  rank,  rank_id,  dist)
        values (:term, :miss, :rank, :rank_id, :dist)
        """
    with sqlite3.connect(spell_db) as cxn:
        cxn.executemany(insert, batch)


def get_spell_check(full_names, delete_chars):
    batch = []
    for name, rank, rank_id in tqdm(full_names):
        batch.append(
            {
                "term": name,
                "miss": name,
                "rank": rank,
                "rank_id": rank_id,
                "dist": 0,
            }
        )

        for miss in deletes1(name):
            batch.append(
                {
                    "term": name,
                    "miss": miss,
                    "rank": rank,
                    "rank_id": rank_id,
                    "dist": 1,
                }
            )

        if delete_chars > 1:
            for miss in deletes2(name):
                batch.append(
                    {
                        "term": name,
                        "miss": miss,
                        "rank": rank,
                        "rank_id": rank_id,
                        "dist": 2,
                    }
                )

    return batch


def deletes1(word: str) -> set[str]:
    return {word[:i] + word[i + 1 :] for i in range(len(word))}


def deletes2(word: str) -> set[str]:
    return {d2 for d1 in deletes1(word) for d2 in deletes1(d1)}


def get_full_names(name_parts):
    full_names = []
    used = set()

    for parts, (rank, rank_id) in name_parts.items():
        add_patterns(parts, rank, rank_id, full_names, used)

    return full_names


def add_patterns(parts, rank, rank_id, batch, used):
    ind1, name1, ind2, name2, ind3, name3, ind4, name4 = parts

    if "x" in (ind1, ind2, ind3, ind4):
        return

    for name in (name1, name2, name3, name4):
        if name.startswith("("):
            return

    abbrev = [f"{name1[0]}.", ind2, name2, ind3, name3, ind4, name4]

    pattern = " ".join(p for p in parts if p)
    add_pattern(pattern, rank, rank_id, batch, used)

    if rank_id >= SPECIES_ID:
        pattern = " ".join(a for a in abbrev if a)
        add_pattern(pattern, rank, rank_id, batch, used)

    # Trinomial without the "ssp."
    if rank_id == SUBSPECIES_ID:
        pattern = " ".join(p for p in parts if p and p != "ssp.")
        add_pattern(pattern, rank, rank_id, batch, used)

        # Abbreviated
        pattern = " ".join(a for a in abbrev if a and a != "ssp.")
        add_pattern(pattern, rank, rank_id, batch, used)


def add_pattern(pattern, rank, rank_id, batch, used):
    if pattern not in used:
        batch.append((pattern, rank, rank_id, rank_id))
        used.add(pattern)


def get_taxon_name_parts(new_taxa, ranks):
    """Get the taxa name parts and the rank of the taxon."""
    name_parts = {}

    for term in new_taxa:
        key = tuple(term[c].lower() if term[c] else "" for c in COLS)

        rank_id = term["rank_id"]

        name_parts[key] = (ranks[rank_id]["rank_name"].lower(), rank_id)

    return name_parts


def get_new_taxa(itis_db):
    with sqlite3.connect(itis_db) as cxn:
        cxn.row_factory = sqlite3.Row

        sql = "select * from taxon_unit_types where kingdom_id = ?"
        ranks = {r["rank_id"]: dict(r) for r in cxn.execute(sql, (KINGDOM_ID,))}

        sql = "select * from taxonomic_units where kingdom_id = ?"
        new_taxa = [t for t in cxn.execute(sql, (KINGDOM_ID,))]

    return new_taxa, ranks


def parse_args():
    description = """Build a database for spellchecking taxa from ITIS terms."""
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description), fromfile_prefix_chars="@"
    )

    arg_parser.add_argument(
        "--itis-db",
        type=Path,
        required=True,
        metavar="PATH",
        help="""Get terms from this ITIS database.""",
    )

    arg_parser.add_argument(
        "--spell-db",
        type=Path,
        required=True,
        metavar="PATH",
        help="""Write the spellchecker terms to this database.""",
    )

    arg_parser.add_argument(
        "--delete-chars",
        type=int,
        choices=[1, 2],
        default=2,
        metavar="INT",
        help="""Build spellchecker terms by deleting this many characters from each
            taxon name. Lower uses less space/memory. (default: %(default)s)""",
    )

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    main()
