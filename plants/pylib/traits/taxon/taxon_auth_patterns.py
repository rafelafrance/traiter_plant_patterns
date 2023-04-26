from traiter.pylib import const as t_const
from traiter.pylib.traits.pattern_compiler import Compiler

from .taxon_action import AND
from .taxon_action import TAXON_LABELS
from .taxon_auth_action import TAXON_AUTH_MATCH
from .taxon_auth_action import TAXON_LINNAEUS_MATCH
from .taxon_auth_action import TAXON_NOT_LINNAEUS_MATCH

LINNAEUS = ["l", "l.", "lin", "lin.", "linn", "linn.", "linnaeus"]


def taxon_auth_patterns():
    decoder = {
        "(": {"TEXT": {"IN": t_const.OPEN}},
        ")": {"TEXT": {"IN": t_const.CLOSE}},
        "and": {"LOWER": {"IN": AND}},
        "auth": {"SHAPE": {"IN": t_const.NAME_SHAPES}},
        "is_auth": {"ENT_TYPE": "is_auth"},
        "linnaeus": {"ENT_TYPE": "linnaeus"},
        "taxon": {"ENT_TYPE": {"IN": TAXON_LABELS}},
        "_": {"TEXT": {"IN": list(":._;,")}},
    }

    return [
        Compiler(
            label="auth1",
            id="taxon",
            on_match=TAXON_AUTH_MATCH,
            keep="taxon",
            decoder=decoder,
            patterns=[
                "taxon ( auth+             _? )",
                "taxon ( auth+ and   auth+ _? )",
                "taxon ( auth+             _? ) auth",
                "taxon ( auth+ and   auth+ _? ) auth auth",
                "taxon   auth                  ",
                "taxon   auth        auth      ",
                "taxon   auth+ and   auth      ",
            ],
        ),
    ]


def taxon_linnaeus_patterns():
    decoder = {
        "(": {"TEXT": {"IN": t_const.OPEN}},
        ")": {"TEXT": {"IN": t_const.CLOSE}},
        ".": {"TEXT": {"IN": t_const.DOT}},
        "auth": {"SHAPE": {"IN": t_const.NAME_SHAPES}},
        "L.": {"TEXT": {"REGEX": r"^L[.,_]$"}},
        "linnaeus": {"LOWER": {"IN": LINNAEUS}},
        "taxon": {"ENT_TYPE": {"IN": TAXON_LABELS}},
    }

    return [
        Compiler(
            label="linnaeus",
            on_match=TAXON_LINNAEUS_MATCH,
            keep="taxon",
            decoder=decoder,
            patterns=[
                "taxon ( linnaeus )",
                "taxon   linnaeus ",
            ],
        ),
        Compiler(
            label="not_linnaeus",
            on_match=TAXON_NOT_LINNAEUS_MATCH,
            keep="taxon",
            decoder=decoder,
            patterns=[
                "taxon L. .? auth",
            ],
        ),
    ]
