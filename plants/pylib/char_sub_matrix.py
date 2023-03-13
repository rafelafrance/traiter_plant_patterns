import csv

from . import const


def get_char_sub_scores():
    vocab_csv = const.VOCAB_DIR / "char_sub_matrix.csv"
    with open(vocab_csv) as vocab_file:
        reader = csv.DictReader(vocab_file)
        rows = list(reader)
    return {(r["char1"], r["char2"]): (r["sub"], r["score"]) for r in rows}
