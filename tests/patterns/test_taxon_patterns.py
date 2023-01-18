import unittest

from tests.setup import test


class TestTaxon(unittest.TestCase):
    def test_taxon_01(self):
        self.assertEqual(
            test("""M. sensitiva"""),
            [
                {
                    "level": "species",
                    "taxon": "M. sensitiva",
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
                    "level": "species",
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
                    "level": "variety",
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
                    "level": "subspecies",
                    "taxon": "A. pachyphloia subsp. brevipinnula",
                    "trait": "taxon",
                    "start": 0,
                    "end": 34,
                }
            ],
        )

    def test_taxon_05(self):
        self.assertEqual(
            test("""M. pachyphloia Bamehy 184."""),
            [
                {
                    "authority": "Bamehy",
                    "level": "species",
                    "taxon": "M. pachyphloia",
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
                    "authority": "Britton & Rose",
                    "level": "species",
                    "taxon": "A. pachyphloia",
                    "trait": "taxon",
                    "start": 0,
                    "end": 29,
                }
            ],
        )

    def test_taxon_07(self):
        self.assertEqual(
            test("""Af. pachyphloia"""),
            [
                {
                    "level": "species",
                    "taxon": "Af. pachyphloia",
                    "trait": "taxon",
                    "start": 0,
                    "end": 15,
                }
            ],
        )
