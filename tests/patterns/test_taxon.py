import unittest

from tests.setup import test


class TestTaxon(unittest.TestCase):
    def test_taxon_00(self):
        test("""Cornus obliqua (Beth.)""")

    def test_taxon_01(self):
        self.assertEqual(
            test("""M. sensitiva"""),
            [
                {
                    "rank": "species",
                    "taxon": "Mimosa sensitiva",
                    "trait": "taxon",
                    "start": 0,
                    "end": 12,
                }
            ],
        )

    def test_taxon_02(self):
        self.assertEqual(
            test("""Mimosa sensitiva"""),
            [
                {
                    "rank": "species",
                    "taxon": "Mimosa sensitiva",
                    "trait": "taxon",
                    "start": 0,
                    "end": 16,
                }
            ],
        )

    def test_taxon_03(self):
        self.assertEqual(
            test("""M. polycarpa var. spegazzinii"""),
            [
                {
                    "rank": "variety",
                    "taxon": "M. polycarpa var. spegazzinii",
                    "trait": "taxon",
                    "start": 0,
                    "end": 29,
                }
            ],
        )

    def test_taxon_04(self):
        self.assertEqual(
            test("""A. pachyphloia subsp. brevipinnula."""),
            [
                {
                    "rank": "subspecies",
                    "taxon": "Acacia pachyphloia subsp. brevipinnula",
                    "trait": "taxon",
                    "start": 0,
                    "end": 34,
                }
            ],
        )

    def test_taxon_05(self):
        self.assertEqual(
            test("""A. pachyphloia Bamehy 184."""),
            [
                {
                    "authority": "Bamehy",
                    "rank": "species",
                    "taxon": "Acacia pachyphloia",
                    "trait": "taxon",
                    "start": 0,
                    "end": 21,
                }
            ],
        )

    def test_taxon_06(self):
        self.assertEqual(
            test("""A. pachyphloia Britton & Rose"""),
            [
                {
                    "authority": "Britton and Rose",
                    "rank": "species",
                    "taxon": "Acacia pachyphloia",
                    "trait": "taxon",
                    "start": 0,
                    "end": 29,
                }
            ],
        )

    def test_taxon_07(self):
        self.assertEqual(
            test("""Ser. Vulpinae is characterized"""),
            [
                {
                    "rank": "series",
                    "taxon": "Vulpinae",
                    "trait": "taxon",
                    "start": 0,
                    "end": 13,
                }
            ],
        )

    def test_taxon_08(self):
        self.assertEqual(
            test("""All species are trees"""),
            [{"end": 21, "part": "trees", "start": 16, "trait": "part"}],
        )

    def test_taxon_09(self):
        self.assertEqual(
            test("""Alajuela, between La Palma and Rio Platanillo"""),
            [],
        )

    def test_taxon_10(self):
        self.assertEqual(
            test("""together with A. pachyphloia (Vulpinae)"""),
            [
                {
                    "taxon": "Acacia pachyphloia",
                    "rank": "species",
                    "trait": "taxon",
                    "start": 14,
                    "end": 28,
                },
                {
                    "taxon": "Vulpinae",
                    "rank": "section",
                    "trait": "taxon",
                    "start": 30,
                    "end": 38,
                },
            ],
        )

    def test_taxon_11(self):
        self.assertEqual(
            test("""Mimosa sensitiva (Bentham) Fox, Trans."""),
            [
                {
                    "authority": "Bentham Fox",
                    "rank": "species",
                    "taxon": "Mimosa sensitiva",
                    "trait": "taxon",
                    "start": 0,
                    "end": 30,
                }
            ],
        )

    def test_taxon_12(self):
        self.assertEqual(
            test(
                """
                Neptunia gracilis f. gracilis Neptunia gracilis var. villosula Benth.,
                """
            ),
            [
                {
                    "taxon": "Neptunia gracilis f. gracilis",
                    "rank": "form",
                    "trait": "taxon",
                    "start": 0,
                    "end": 29,
                },
                {
                    "taxon": "Neptunia gracilis var. villosula",
                    "rank": "variety",
                    "authority": "Benth",
                    "trait": "taxon",
                    "start": 30,
                    "end": 68,
                },
            ],
        )

    def test_taxon_13(self):
        """It handles 'F.' genus abbreviation vs 'f.' form abbreviation."""
        self.assertEqual(
            test(
                """
                F. gracilis Neptunia gracilis var. villosula Benth.,
                """
            ),
            [
                {
                    "taxon": "F. gracilis",
                    "rank": "species",
                    "trait": "taxon",
                    "start": 0,
                    "end": 11,
                },
                {
                    "taxon": "Neptunia gracilis var. villosula",
                    "rank": "variety",
                    "authority": "Benth",
                    "trait": "taxon",
                    "start": 12,
                    "end": 50,
                },
            ],
        )

    def test_taxon_14(self):
        self.assertEqual(
            test("""Ticanto rhombifolia"""),
            [
                {
                    "taxon": "Ticanto rhombifolia",
                    "rank": "species",
                    "trait": "taxon",
                    "start": 0,
                    "end": 19,
                }
            ],
        )

    def test_taxon_15(self):
        """It gets a taxon notation."""
        self.assertEqual(
            test(
                """
                Cornaceae
                Cornus obliqua Raf.
                """
            ),
            [
                {
                    "rank": "family",
                    "taxon": "Cornaceae",
                    "trait": "taxon",
                    "start": 0,
                    "end": 9,
                },
                {
                    "authority": "Raf",
                    "rank": "species",
                    "taxon": "Cornus obliqua",
                    "trait": "taxon",
                    "start": 10,
                    "end": 28,
                },
            ],
        )

    def test_taxon_16(self):
        """It gets a family notation."""
        self.assertEqual(
            test(
                """
                Crowley's Ridge
                Fabaceae
                Vicia villosa Roth ssp. varia (Khan)
                """
            ),
            [
                {
                    "taxon": "Fabaceae",
                    "rank": "family",
                    "trait": "taxon",
                    "start": 16,
                    "end": 24,
                },
                {
                    "taxon": "Vicia villosa subsp. varia",
                    "rank": "subspecies",
                    "authority": ["Roth", "Khan"],
                    "trait": "taxon",
                    "start": 25,
                    "end": 61,
                },
            ],
        )

    def test_taxon_17(self):
        """It gets the full notation."""
        self.assertEqual(
            test("""Cephalanthus occidentalis L. Rubiaceas"""),
            [
                {
                    "taxon": "Cephalanthus occidentalis",
                    "rank": "species",
                    "authority": "L. Rubiaceas",
                    "trait": "taxon",
                    "start": 0,
                    "end": 38,
                }
            ],
        )

    def test_taxon_18(self):
        """It handles 'f.' form abbreviation vs 'F.' genus abbreviation."""
        self.assertEqual(
            test("""A. pachyphloia f. brevipinnula."""),
            [
                {
                    "rank": "form",
                    "taxon": "Acacia pachyphloia f. brevipinnula",
                    "trait": "taxon",
                    "start": 0,
                    "end": 30,
                }
            ],
        )
