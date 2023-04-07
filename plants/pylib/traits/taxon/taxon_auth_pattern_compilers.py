from pathlib import Path

from traiter.pylib import const as t_const
from traiter.pylib.traits import trait_util
from traiter.pylib.traits.pattern_compiler import Compiler

RANK_CSV = Path(__file__).parent / "rank_terms.csv"

RANK_TERMS = trait_util.read_terms(RANK_CSV)
LOWER_RANK = sorted({r["label"] for r in RANK_TERMS if r["level"] == "lower"})

AND = ["&", "and", "et"]
LINNAEUS = ["l", "l.", "lin", "lin.", "linn", "linn.", "linnaeus"]


def taxon_auth_compilers():
    decoder = {
        "(": {"TEXT": {"IN": t_const.OPEN}},
        ")": {"TEXT": {"IN": t_const.CLOSE}},
        "and": {"LOWER": {"IN": AND}},
        "auth": {"SHAPE": {"IN": t_const.NAME_SHAPES}},
        "is_auth": {"ENT_TYPE": "is_auth"},
        "linnaeus": {"ENT_TYPE": "linnaeus"},
        "taxon": {"ENT_TYPE": "taxon"},
        # "linnaeus": {"_": {"flag": {"REGEX": "linnaeus"}}},
        # "taxon": {"_": {"flag": {"REGEX": "taxon"}}},
        "_": {"TEXT": {"IN": list(":._;,")}},
    }

    return [
        Compiler(
            label="taxon",
            id="auth1",
            decoder=decoder,
            patterns=[
                "taxon ( auth+             _? )",
                "taxon ( auth+ and   auth+ _? )",
                "taxon   auth                  ",
                "taxon   auth  auth            ",
                "taxon   auth+ and   auth      ",
                "linnaeus+",
                "is_auth+",
            ],
        ),
    ]


def taxon_linnaeus_compilers():
    decoder = {
        "(": {"TEXT": {"IN": t_const.OPEN}},
        ")": {"TEXT": {"IN": t_const.CLOSE}},
        ".": {"TEXT": {"IN": t_const.DOT}},
        "auth": {"SHAPE": {"IN": t_const.NAME_SHAPES}},
        "L.": {"TEXT": {"REGEX": r"^L[.,_]$"}},
        "linnaeus": {"LOWER": {"IN": LINNAEUS}},
        "taxon": {"ENT_TYPE": "taxon"},
    }

    return [
        Compiler(
            label="linnaeus",
            id="linnaeus",
            decoder=decoder,
            patterns=[
                "taxon ( linnaeus )",
                "taxon   linnaeus ",
            ],
        ),
        Compiler(
            label="is_auth",
            decoder=decoder,
            patterns=[
                "taxon L. .? auth",
                "taxon L. .? auth auth",
            ],
        ),
    ]
