import sqlite3

from . import const


def get_char_sub_scores():
    with sqlite3.connect(const.CHAR_DB) as cxn:
        cxn.row_factory = sqlite3.Row
        rows = cxn.execute("select * from char_sub_matrix")
        scores = {(r["char1"], r["char2"]): (r["sub"], r["score"]) for r in rows}
    return scores
