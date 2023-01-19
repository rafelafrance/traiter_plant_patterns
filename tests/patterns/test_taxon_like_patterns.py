import unittest

from tests.setup import test


class TestTaxonLike(unittest.TestCase):
    def test_taxon_like_01(self):
        self.assertEqual(
            test("""it seems closer to the nearly sympatric M. sensitiva."""),
            [
                {
                    "level": "species",
                    "taxon_like": "M. sensitiva",
                    "trait": "taxon_like",
                    "start": 30,
                    "end": 52,
                    "relation": "sympatric",
                }
            ],
        )

    def test_taxon_like_02(self):
        self.assertEqual(
            test("""it is similar to M. sensitiva."""),
            [
                {
                    "level": "species",
                    "taxon_like": "M. sensitiva",
                    "trait": "taxon_like",
                    "start": 6,
                    "end": 29,
                    "relation": "similar",
                }
            ],
        )

    def test_taxon_like_03(self):
        self.assertEqual(
            test("""It resembles M. sensitiva in amplitude"""),
            [
                {
                    "level": "species",
                    "taxon_like": "M. sensitiva",
                    "trait": "taxon_like",
                    "start": 3,
                    "end": 25,
                    "relation": "resembles",
                }
            ],
        )

    def test_taxon_like_04(self):
        self.assertEqual(
            test("""sympatric pair of M. sensitiva Harms ex Glaziou"""),
            [
                {
                    "level": "species",
                    "authority": "Harms Glaziou",
                    "taxon_like": "M. sensitiva",
                    "trait": "taxon_like",
                    "start": 0,
                    "end": 47,
                    "relation": "sympatric",
                }
            ],
        )

    def test_taxon_like_05(self):
        self.assertEqual(
            test("""vicinis M. sensitiva et M. pachyphloia"""),
            [
                {
                    "level": "species",
                    "taxon_like": ["M. sensitiva", "M. pachyphloia"],
                    "trait": "taxon_like",
                    "start": 0,
                    "end": 38,
                    "relation": "vicinis",
                }
            ],
        )

    def test_taxon_like_06(self):
        self.assertEqual(
            test("""distinguished from var. pachyphloia"""),
            [
                {
                    "level": "variety",
                    "trait": "taxon_like",
                    "start": 0,
                    "end": 35,
                    "taxon_like": "var. pachyphloia",
                    "relation": "distinguished",
                }
            ],
        )

    def test_taxon_like_07(self):
        self.assertEqual(
            test("""The var. floridana resembles var. nuttallii in venation"""),
            [
                {
                    "level": "variety",
                    "taxon": "var. floridana",
                    "trait": "taxon",
                    "start": 4,
                    "end": 18,
                    "taxon_like": "var. nuttallii",
                },
                {
                    "level": "variety",
                    "trait": "taxon_like",
                    "start": 19,
                    "end": 43,
                    "taxon_like": "var. nuttallii",
                    "relation": "resembles",
                },
                {"venation": "vein", "trait": "venation", "start": 47, "end": 55},
            ],
        )
