import pandas as pd

from ..patterns import term_patterns as terms

EXTRAS = set(""" sex location group """.split())

SKIP = {"trait", "start", "end", "dimensions", "taxon"}
SKIP |= EXTRAS | terms.PARTS_SET | terms.SUBPART_SET


class CsvWriter:
    def __init__(self):
        self.csv_rows = []

    def write(self, rows, out_csv):
        csv_rows = [self.format_row(r) for r in rows]
        df = pd.DataFrame(csv_rows).fillna("")
        df = self.sort_columns(df)
        df.to_csv(out_csv, index=False)

    def format_row(self, row):
        raise NotImplementedError()

    @staticmethod
    def sort_columns(df):
        return df
