from traiter.pylib.term_list import TermList

from .. import const

BASIC_TERMS = TermList.shared("units")
BASIC_TERMS += TermList.shared("numerics")
BASIC_TERMS += TermList.read(const.VOCAB_DIR / "treatment.csv")

BASIC_TERMS.drop("imperial_length")
BASIC_TERMS.drop("time_units")
BASIC_TERMS.drop("ordinal numeric_units roman")

SUFFIX_TERMS = BASIC_TERMS.pattern_dict("suffix_term")
