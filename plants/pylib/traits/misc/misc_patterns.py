from traiter.pylib.traits.pattern_compiler import Compiler

from .misc_action import LABELS
from .misc_action import MISC_MATCH


def misc_patterns():
    return [
        Compiler(
            label="misc",
            on_match=MISC_MATCH,
            decoder={"term": {"ENT_TYPE": {"IN": LABELS}}},
            patterns=[" term+ "],
        ),
    ]
