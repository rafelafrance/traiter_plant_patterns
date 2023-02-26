import os

from plants.pylib import const

# Some test taxa are in the term DB for testing
if "ALL_TAXA" not in os.environ:
    const.TAXON_DB = const.TERM_DB
