from pathlib import Path

from traiter.pylib import const as t_const
from traiter.pylib.traits import trait_util
from traiter.pylib.traits.pattern_compiler import Compiler


HERE = Path(__file__).parent
TRAIT = HERE.stem

CSV = HERE / f"{TRAIT}.csv"

NOT_PART = ["part_and", "part_leader", "part_missing", "subpart"]
PART_LABELS = [lb for lb in trait_util.get_labels(CSV) if lb not in NOT_PART]

DECODER = {
    "-": {"TEXT": {"IN": t_const.DASH}, "OP": "+"},
    "and": {"ENT_TYPE": "part_and"},
    "leader": {"ENT_TYPE": "part_leader"},
    "missing": {"ENT_TYPE": "missing"},
    "part": {"ENT_TYPE": {"IN": PART_LABELS}},
    "subpart": {"ENT_TYPE": "subpart"},
}

COMPILERS = [
    Compiler(
        label="part",
        decoder=DECODER,
        patterns=[
            "leader? part",
            "leader? part - part",
        ],
    ),
    Compiler(
        label="missing_part",
        decoder=DECODER,
        patterns=[
            "missing part and part",
            "missing part",
            "missing part -   part",
        ],
    ),
    Compiler(
        label="multiple_parts",
        decoder=DECODER,
        patterns=[
            "leader? part+ and part+",
            "missing part+ and part+",
        ],
    ),
    Compiler(
        label="subpart",
        decoder=DECODER,
        patterns=[
            "leader? subpart",
            "leader? subpart - subpart",
            "leader? part -?   subpart",
            "leader? part      subpart",
            "- subpart",
        ],
    ),
    # Compiler(
    #     label="missing_subpart",
    #     decoder=DECODER,
    #     patterns=[
    #         "missing part -?   subpart",
    #         "missing part      subpart",
    #         "missing subpart",
    #     ],
    # ),
]
