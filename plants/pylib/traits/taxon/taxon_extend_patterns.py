from traiter.pylib import const as t_const
from traiter.pylib.traits.pattern_compiler import Compiler

from .taxon_action import AND
from .taxon_action import LOWER_RANK
from .taxon_action import MAYBE
from .taxon_action import TAXON_LABELS_LINNAEUS
from .taxon_extend_action import TAXON_EXTEND_MATCH


def taxon_extend_patterns():
    return [
        Compiler(
            label="extend",
            id="taxon",
            on_match=TAXON_EXTEND_MATCH,
            decoder={
                "(": {"TEXT": {"IN": t_const.OPEN}},
                ")": {"TEXT": {"IN": t_const.CLOSE}},
                "and": {"LOWER": {"IN": AND}},
                "auth": {"SHAPE": {"IN": t_const.NAME_SHAPES}},
                "maybe": {"POS": {"IN": MAYBE}},
                "taxon": {"ENT_TYPE": {"IN": TAXON_LABELS_LINNAEUS}},
                "lower_rank": {"ENT_TYPE": {"IN": LOWER_RANK}},
            },
            patterns=[
                "taxon lower_rank+ taxon",
                "taxon lower_rank+ taxon ( auth+                       )",
                "taxon lower_rank+ taxon ( auth+ maybe auth+           )",
                "taxon lower_rank+ taxon ( auth+             and auth+ )",
                "taxon lower_rank+ taxon ( auth+ maybe auth+ and auth+ )",
                "taxon lower_rank+ taxon   auth+                        ",
                "taxon lower_rank+ taxon   auth+ maybe auth+            ",
                "taxon lower_rank+ taxon   auth+             and auth+  ",
                "taxon lower_rank+ taxon   auth+ maybe auth+ and auth+  ",
                "taxon lower_rank+ maybe",
                "taxon lower_rank+ maybe ( auth+                       )",
                "taxon lower_rank+ maybe ( auth+ maybe auth+           )",
                "taxon lower_rank+ maybe ( auth+             and auth+ )",
                "taxon lower_rank+ maybe ( auth+ maybe auth+ and auth+ )",
                "taxon lower_rank+ maybe   auth+                        ",
                "taxon lower_rank+ maybe   auth+ maybe auth+            ",
                "taxon lower_rank+ maybe   auth+             and auth+  ",
                "taxon lower_rank+ maybe   auth+ maybe auth+ and auth+  ",
            ],
        ),
    ]
