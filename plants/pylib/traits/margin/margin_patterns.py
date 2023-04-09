from traiter.pylib import const as t_const
from traiter.pylib.traits.pattern_compiler import Compiler

from .margin_action import MARGIN_MATCH


def margin_patterns():
    return [
        Compiler(
            label="margin",
            on_match=MARGIN_MATCH,
            decoder={
                "-": {"TEXT": {"IN": t_const.DASH}},
                "margin": {"ENT_TYPE": "margin"},
                "shape": {"ENT_TYPE": "shape"},
                "leader": {"ENT_TYPE": {"IN": ["shape", "margin_leader"]}},
                "follower": {"ENT_TYPE": {"IN": ["margin", "margin_follower"]}},
            },
            patterns=[
                "leader* -* margin+",
                "leader* -* margin -* follower*",
                "leader* -* margin -* shape? follower+ shape?",
                "shape+ -* follower+",
            ],
        ),
    ]
