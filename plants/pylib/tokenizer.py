import re

from spacy.lang.char_classes import ALPHA
from spacy.lang.char_classes import LIST_HYPHENS
from spacy.lang.char_classes import LIST_PUNCT
from spacy.lang.char_classes import LIST_QUOTES
from traiter.pylib import const as t_const
from traiter.pylib import tokenizer_util

BREAKING = LIST_QUOTES + LIST_PUNCT + [r"[:\\/˂˃×.+’()\[\]±_]"]

CLOSES = "|".join(re.escape(h) for h in t_const.CLOSE if len(h) == 1)
CLOSES = f"(?:{CLOSES})"

DASHES = "|".join(re.escape(h) for h in LIST_HYPHENS if len(h) == 1)
DASHES = f"(?:{DASHES})+"

OPENS = "|".join(re.escape(h) for h in t_const.OPEN if len(h) == 1)
OPENS = f"(?:{OPENS})"

_PREFIX = BREAKING + [DASHES + "(?=[0-9])"]
_SUFFIX = BREAKING + [DASHES]


_INFIX = [
    rf"(?<=[{ALPHA}0-9])[:<>=/+](?=[{ALPHA}])",  # word=word etc.
    r"""[\\\[\]()/:;’'“”'+±_]""",  # Break on these characters
    DASHES,
    rf"(?<=\d)[{ALPHA}]+",
]


def setup_tokenizer(nlp):
    tokenizer_util.append_prefix_regex(nlp, _PREFIX)
    tokenizer_util.append_infix_regex(nlp, _INFIX)
    tokenizer_util.append_suffix_regex(nlp, _SUFFIX)
    # Remove patterns that interfere with numerical parses
    removes = []
    for rule in nlp.tokenizer.rules:
        if re.search(r"\d", rule) and not re.search(r"m\.?$", rule):
            removes.append(rule)
    tokenizer_util.remove_special_case(nlp, removes)
