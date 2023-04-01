from traiter.pylib import const as t_const
from traiter.pylib.traits.pattern_compiler import Compiler

LEADERS = """ shape margin_leader """.split()
FOLLOWERS = """ margin margin_follower """.split()

COMPILERS = [
    Compiler(
        label="margin",
        decoder={
            "-": {"TEXT": {"IN": t_const.DASH}},
            "margin": {"ENT_TYPE": "margin"},
            "shape": {"ENT_TYPE": "shape"},
            "leader": {"ENT_TYPE": {"IN": LEADERS}},
            "follower": {"ENT_TYPE": {"IN": FOLLOWERS}},
        },
        patterns=[
            "leader* -* margin+",
            "leader* -* margin -* follower*",
            "leader* -* margin -* shape? follower+ shape?",
            "shape+ -* follower+",
        ],
    ),
]
