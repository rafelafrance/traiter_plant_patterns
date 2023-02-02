"""Get mimosa taxon notations."""
import regex as re
from spacy import registry
from traiter.pylib import actions
from traiter.pylib.patterns.matcher_patterns import MatcherPatterns

from . import common_patterns
from . import term_patterns
from .. import const

M_DOT = r"^[A-Z][a-z]?\.?$"
M_DOT_RE = re.compile(M_DOT)

REJECT_LEVEL = """ name names group groups level levels pattern patterns """.split()

DECODER = common_patterns.COMMON_PATTERNS | {
    "auth": {"SHAPE": {"IN": const.NAME_SHAPES}},
    "maybe": {"POS": {"IN": ["PROPN", "NOUN"]}},
    "taxon": {"ENT_TYPE": "plant_taxon"},
    "level": {"ENT_TYPE": "level"},
    "M.": {"TEXT": {"REGEX": M_DOT}},
}


def build_taxon(span):
    auth = []
    used_levels = []
    taxa = []
    original = []
    is_level = ""
    data = {}

    for token in span:
        if token._.cached_label == "level":
            taxa.append(token.lower_)
            original.append(token.text)
            is_level = token.lower_
            data["level"] = term_patterns.REPLACE.get(token.lower_, token.lower_)

        elif is_level:
            if token.lower_ not in REJECT_LEVEL:
                if data["level"] in const.LOWER_TAXON_LEVEL:
                    original.append(token.text)
                    taxa.append(token.lower_)
                else:
                    original.append(token.text)
                    taxa.append(token.text.title())
            is_level = ""

        elif M_DOT_RE.match(token.text):
            original.append(token.text)
            taxa.append(token.text)
            used_levels.append("genus")

        elif token.text == ".":
            taxa.append(taxa.pop() + ".")

        elif token._.cached_label == "plant_taxon":
            levels = term_patterns.LEVELS.get(token.lower_, ["unknown"])

            # Find the highest unused taxon level
            for level in levels:
                if level not in used_levels:
                    used_levels.append(level)
                    data["level"] = level
                    if level in const.LOWER_TAXON_LEVEL:
                        original.append(token.text)
                        taxa.append(token.lower_)
                    else:
                        original.append(token.text)
                        taxa.append(token.text.title())
                    break
            else:
                original.append(token.text)
                taxa.append(token.text)

        elif token.pos_ in ["PROPN", "NOUN"] or token.lower_ in common_patterns.AND:
            if token.shape_ in const.TITLE_SHAPES:
                auth.append(token.text)
            elif auth and token.lower_ in common_patterns.AND:
                auth.append(token.text)

    if auth:
        data["authority"] = " ".join(auth)

    data["taxon"] = " ".join([t for t in taxa if t])

    return data, original


def cleanup_ent(ent, original):
    if ent._.data.get("plant_taxon"):
        del ent._.data["plant_taxon"]

    # There is latin in the text, I need to guard against that
    is_lower = ent._.data.get("level") in const.LOWER_TAXON_LEVEL
    alone = len(ent._.data["taxon"].split()) == 1
    if alone and (is_lower or original[0][0].islower()):
        ent._.delete = True
        raise actions.RejectMatch()


# ###################################################################################
MULTI_TAXON = MatcherPatterns(
    "multi_taxon",
    on_match="plant_multi_taxon_v1",
    decoder=DECODER,
    patterns=[
        "M.? taxon+ and M.? taxon+",
    ],
)


@registry.misc(MULTI_TAXON.on_match)
def on_multi_taxon_match(ent):
    conj_idx = next(i for i, t in enumerate(ent) if t.lower_ in common_patterns.AND)
    first, _ = build_taxon(ent[:conj_idx])
    ent._.data = {
        "level": first["level"],
        "taxon": [first["taxon"]],
    }
    second, _ = build_taxon(ent[conj_idx + 1 :])
    ent._.data["taxon"].append(second["taxon"])


# ###################################################################################
TAXON = MatcherPatterns(
    "taxon",
    on_match="plant_taxon_v1",
    decoder=DECODER,
    patterns=[
        "M.? taxon+ (? auth*                       )?",
        "M.? taxon+ (? auth+ maybe auth+           )?",
        "M.? taxon+ (? auth*                       )? level .? maybe",
        "M.? taxon+ (? auth+ maybe auth+           )? level .? maybe",
        "M.? taxon+ (? auth*             and auth+ )?",
        "M.? taxon+ (? auth+ maybe auth+ and auth+ )?",
        "M.? taxon+ (? auth*             and auth+ )? level .? maybe",
        "M.? taxon+ (? auth+ maybe auth+ and auth+ )? level .? maybe",
        "level .? taxon+",
        "level .? maybe",
        "taxon+",
        "M.? taxon level .? maybe",
        "M. .? taxon+",
    ],
)


@registry.misc(TAXON.on_match)
def on_taxon_match(ent):
    ent._.data, original = build_taxon(ent)
    cleanup_ent(ent, original)
