import string

import regex as re
from spacy.util import registry
from traiter import tokenizer_util

ABBREVS = """
    Jan. Feb. Febr. Mar. Apr. Jun. Jul. Aug. Sep. Sept. Oct. Nov. Dec.
    Var. Sect. Subsect. Ser. Subser. Subsp. Spec. Sp. Spp.
    var. sect. subsect. ser. subser. subsp. spec. sp. spp. nov.
    Acad. Agri. Amer. Ann. Arb. Arq. adj. al. alt. ann.
    Bol. Bot. Bras. Bull. bot. bras.
    Cat. Ci. Coll. Columb. Com. Contr. Cur. ca. cent. centr. cf. coll.
    DC. depto. diam. dtto.
    Encycl. Encyle. Exot. ed. ememd. ent. est.
    FIG. Fig. Figs. Fl. fig. figs. fl. flor. flumin.
    Gard. Gen. Geo. gard. geograph.
    Herb. Hist. Hort. hb. hist.
    Is. illeg. infra. is.
    Jahrb. Jard. Jr. jug.
    Lab. Lam. Leg. Legum. Linn. lam. lat. leg. lin. long.
    Mag. Mem. Mex. Mts. Mus. Nac. mem. mens. monac. mont. mun.
    Nat. Natl. Neg. No. nat. no. nom. nud.
    Ocas.
    PI. PL. Pl. Proc. Prodr. Prov. Pt. Pto. Publ. p. pi. pl. pr. prov.
    reg. revis.
    Sa. Sci. Soc. Sr. Sta. Sto. Sul. Suppl. Syst.
    s. sci. stat. stk. str. superfl. suppl. surv. syn.
    Tex. Trans telegr.
    U.S. US. Univ.
    Veg. veg.
    Wm.
    I. II. III. IV. IX. V. VI. VII. VIII. X. XI. XII. XIII. XIV. XIX. XV. XVI. XVII.
    XVIII. XX. XXI. XXII. XXIII. XXIV. XXV.
    i. ii. iii. iv. ix. v. vi. vii. viii. x. xi. xii. xiii. xiv. xix. xv. xvi. xvii.
    xviii. xx. xxi. xxii. xxiii. xxiv. xxv.
    """.split()
ABBREVS += [f"{c}." for c in string.ascii_uppercase]

TOKENIZER = "plant_custom_tokenizer_v1"


def setup_tokenizer(nlp):
    not_letter = re.compile(r"[^a-zA-Z.']")
    removes = [{"pattern": s} for s in nlp.tokenizer.rules if not_letter.search(s)]
    tokenizer_util.remove_special_case(nlp, removes)
    tokenizer_util.append_tokenizer_regexes(nlp)
    tokenizer_util.append_abbrevs(nlp, ABBREVS)


@registry.callbacks(TOKENIZER)
def make_customized_tokenizer():
    def customized_tokenizer(nlp):
        setup_tokenizer(nlp)

    return customized_tokenizer
