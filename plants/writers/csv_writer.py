from collections import defaultdict

import pandas as pd

from ..patterns import term_patterns as terms

EXTRAS = set(""" sex location group """.split())

SKIP = {"trait", "start", "end", "dimensions", "taxon"}
SKIP |= EXTRAS | terms.PARTS_SET | terms.SUBPART_SET


class CsvWriter:
    def __init__(self, out_csv):
        self.out_csv = out_csv
        self.csv_rows = []

    def write(self, rows):
        csv_rows = self.format_all_rows(rows)
        df = pd.DataFrame(csv_rows).fillna("")
        df = self.sort_df(df)
        df.to_csv(self.out_csv, index=False)

    def format_all_rows(self, rows):
        csv_rows = [self.format_row(r) for r in rows]
        return csv_rows

    def format_row(self, row):
        raise NotImplementedError()

    def row_builder(self, row, csv_row):
        by_header = defaultdict(list)
        for trait in row.traits:
            if trait["trait"] in terms.PARTS_SET:
                continue

            key_set = set(trait.keys())

            if not (terms.PARTS_SET & key_set):
                continue

            base_header = self.base_column_header(trait, key_set)

            self.group_values_by_header(by_header, trait, base_header)
            self.number_columns(by_header, csv_row)
        return csv_row

    @staticmethod
    def sort_df(df):
        return df

    @staticmethod
    def base_column_header(trait, key_set):
        part = (terms.PARTS_SET & key_set).pop()
        if "subpart" in trait:
            label = f'{part}_{trait["subpart"]}_{trait["trait"]}'
        elif "subpart_suffix" in trait:
            subpart = trait["subpart_suffix"].removeprefix("-")
            label = f'{part}_{subpart}_{trait["trait"]}'
        else:
            label = f'{part}_{trait["trait"]}'
        return label

    @staticmethod
    def group_values_by_header(by_header, trait, base_header):
        extras = sorted(v for k, v in trait.items() if k in EXTRAS)
        unnumbered_header = "_".join([base_header] + extras)
        trait = {k: v for k, v in trait.items() if k not in SKIP}
        by_header[unnumbered_header].append(trait)

    @staticmethod
    def number_columns(by_header, csv_row):
        for unnumbered_header, trait_list in by_header.items():
            for i, trait in enumerate(trait_list, 1):
                for key, value in trait.items():
                    header = f"{unnumbered_header}.{i}.{key}"
                    csv_row[header] = value
