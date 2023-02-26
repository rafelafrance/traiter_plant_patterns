#!/usr/bin/env python3
import csv
import sqlite3

from pylib import const
from traiter.pylib import log

CREATE_TERM_DB = """
    CREATE TABLE IF NOT EXISTS term_columns (
        term_set text,
        extra    text,
        rename   text
    );

    CREATE TABLE IF NOT EXISTS terms (
        term_set text,
        label    text,
        pattern  text,
        attr     text,
        replace  blob,
        extra1   blob,
        extra2   blob
    );

    CREATE INDEX IF NOT EXISTS term_column_sets on term_columns (term_set);
    CREATE INDEX IF NOT EXISTS term_labels on terms (label);
    CREATE INDEX IF NOT EXISTS term_patterns on terms (pattern);
    CREATE INDEX IF NOT EXISTS term_sets on terms (term_set);
"""

INSERT_TERM_COLUMNS = """
    insert into term_columns
               ( term_set,  extra,  rename)
        values (:term_set, :extra, :rename)
    """

INSERT_TERMS = """
    insert into terms
               ( term_set,  label,  pattern,  attr,  replace,  extra1,  extra2)
        values (:term_set, :label, :pattern, :attr, :replace, :extra1, :extra2)
    """

CREATE_CHAR_DB = """
    CREATE TABLE IF NOT EXISTS char_sub_matrix (
        char1    TEXT,
        char2    TEXT,
        score    REAL,
        char_set TEXT,
        sub      REAL
);
"""

INSERT_CHARS = """
    insert into char_sub_matrix
           ( char1,  char2,  score,  char_set,  sub)
    values (:char1, :char2, :score, :char_set, :sub)
"""


def main():
    log.started()

    create_term_db()
    create_char_db()

    log.finished()


def create_term_db():
    with open(const.VOCAB_DIR / "term_columns.csv") as in_csv:
        reader = csv.DictReader(in_csv)
        term_columns = [r for r in reader]

    with open(const.VOCAB_DIR / "terms.csv") as in_csv:
        reader = csv.DictReader(in_csv)
        terms = [r for r in reader]

    with sqlite3.connect(const.VOCAB_DIR / "terms.sqlite") as cxn:
        cxn.executescript(CREATE_TERM_DB)
        cxn.executemany(INSERT_TERM_COLUMNS, term_columns)
        cxn.executemany(INSERT_TERMS, terms)


def create_char_db():
    with open(const.VOCAB_DIR / "char_sub_matrix.csv") as in_csv:
        reader = csv.DictReader(in_csv)
        char_sub_matrix = [r for r in reader]

    with sqlite3.connect(const.VOCAB_DIR / "char_sub_matrix.sqlite") as cxn:
        cxn.executescript(CREATE_CHAR_DB)
        cxn.executemany(INSERT_CHARS, char_sub_matrix)


if __name__ == "__main__":
    main()
