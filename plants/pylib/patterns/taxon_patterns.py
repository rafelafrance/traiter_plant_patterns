import regex as re
from spacy import registry
from traiter.pylib import actions
from traiter.pylib.patterns.matcher_patterns import MatcherPatterns

from . import common_patterns
from . import term_patterns
from .. import const

M_DOT = r"^[A-Z][a-z]?\.?$"
M_DOT_RE = re.compile(M_DOT)

MIN_RANK_LEN = 4

REJECT_RANK = """
    name names group groups rank ranks pattern patterns level pair pairs diversity
    relationships salvador sierra local
    """.split()

NOT_A_GENUS = """ la el """.split()

DECODER = common_patterns.COMMON_PATTERNS | {
    "auth": {"SHAPE": {"IN": const.NAME_SHAPES}},
    "maybe": {"POS": {"IN": ["PROPN", "NOUN"]}},
    "nope": {"LOWER": {"IN": NOT_A_GENUS}},
    "taxon": {"ENT_TYPE": "plant_taxon"},
    "rank": {"ENT_TYPE": "rank"},
    "M.": {"TEXT": {"REGEX": M_DOT}},
}


def build_taxon(span):
    auth = []
    used_ranks = []
    taxa = []
    original = []
    is_rank = ""
    data = {}

    for token in span:
        # We got a rank label the next token is the rank
        if token._.cached_label == "rank":
            taxa.append(token.lower_)
            original.append(token.text)
            is_rank = token.lower_
            data["rank"] = term_patterns.REPLACE.get(token.lower_, token.lower_)

        # The last token was a rank label this token should be a rank
        elif is_rank:
            if token.lower_ not in REJECT_RANK:  # and len(token) >= MIN_RANK_LEN:
                if data["rank"] in const.LOWER_TAXON_RANK:
                    original.append(token.text)
                    taxa.append(token.lower_)
                else:
                    original.append(token.text)
                    taxa.append(token.text.title())
            is_rank = ""

        # An abbreviated genus C. lupus
        elif M_DOT_RE.match(token.text):
            original.append(token.text)
            taxa.append(token.text)
            used_ranks.append("genus")

        # We have a taxon name from the DB
        elif token._.cached_label == "plant_taxon":
            ranks = term_patterns.RANKS.get(token.lower_, ["unknown"])

            # Find the highest unused taxon rank
            for rank in ranks:
                if rank not in used_ranks:
                    used_ranks.append(rank)
                    data["rank"] = rank

                    # Capitalize the taxon
                    if rank in const.LOWER_TAXON_RANK:
                        original.append(token.text)
                        taxa.append(token.lower_)
                    else:
                        original.append(token.text)
                        taxa.append(token.text.title())
                    break
            else:
                original.append(token.text)
                taxa.append(token.text)

        # These are maybe an authority
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
    is_lower = ent._.data.get("rank") in const.LOWER_TAXON_RANK
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
        "rank": first["rank"],
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
        "M.? taxon+ (  auth*                       ) ",
        "M.? taxon+ (  auth+ maybe auth+           ) ",
        "M.? taxon+ (  auth*                       )  rank .? maybe",
        "M.? taxon+ (  auth+ maybe auth+           )  rank .? maybe",
        "M.? taxon+ (  auth*             and auth+ ) ",
        "M.? taxon+ (  auth+ maybe auth+ and auth+ ) ",
        "M.? taxon+ (  auth*             and auth+ )  rank .? maybe",
        "M.? taxon+ (  auth+ maybe auth+ and auth+ )  rank .? maybe",
        "M.? taxon+    auth*                         ",
        "M.? taxon+    auth+ maybe auth+             ",
        "M.? taxon+    auth*                          rank .? maybe",
        "M.? taxon+    auth+ maybe auth+              rank .? maybe",
        "M.? taxon+    auth+             and auth+   ",
        "M.? taxon+    auth+ maybe auth+ and auth+   ",
        "M.? taxon+    auth*             and auth+    rank .? maybe",
        "M.? taxon+    auth+ maybe auth+ and auth+    rank .? maybe",
        "rank .? taxon+",
        "rank .? maybe",
        "taxon+",
        "M.?   taxon rank .? maybe",
        "M. .? taxon+",
    ],
)


@registry.misc(TAXON.on_match)
def on_taxon_match(ent):
    ent._.data, original = build_taxon(ent)
    cleanup_ent(ent, original)


# ###################################################################################
NOT_A_TAXON = MatcherPatterns(
    "not_a_taxon",
    on_match=actions.REJECT_MATCH,
    decoder=DECODER,
    patterns=[
        "nope taxon+    auth*                         ",
        "nope taxon+    auth+ maybe auth+             ",
        "nope taxon+    auth*                          rank .? maybe",
        "nope taxon+    auth+ maybe auth+              rank .? maybe",
        "nope taxon+    auth*             and auth+   ",
        "nope taxon+    auth+ maybe auth+ and auth+   ",
        "nope taxon+    auth*             and auth+    rank .? maybe",
        "nope taxon+    auth+ maybe auth+ and auth+    rank .? maybe",
        "taxon and? M.",
    ],
)