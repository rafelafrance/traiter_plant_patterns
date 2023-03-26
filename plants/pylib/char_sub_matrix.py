import csv

from .vocabulary import terms


def get_char_sub_scores():
    vocab_csv = terms.VOCAB_DIR / "char_sub_matrix.csv"
    with open(vocab_csv) as vocab_file:
        reader = csv.DictReader(vocab_file)
        rows = list(reader)
    return {(r["char1"], r["char2"]): (r["sub"], r["score"]) for r in rows}
