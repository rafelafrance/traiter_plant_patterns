import unittest

from tests.setup import test


class TestDescriptor(unittest.TestCase):
    def test_descriptor_01(self):
        self.assertEqual(
            test(
                """
                bisexual (unisexual and plants sometimes gynodioecious,
                or plants dioecious"""
            ),
            [
                {"sex": "bisexual", "trait": "sex", "start": 0, "end": 8},
                {"sex": "unisexual", "trait": "sex", "start": 10, "end": 19},
                {
                    "part": "plant",
                    "trait": "part",
                    "start": 24,
                    "end": 30,
                    "sex": "unisexual",
                },
                {
                    "reproduction": "gynodioecious",
                    "trait": "reproduction",
                    "start": 41,
                    "end": 54,
                    "part": "plant",
                    "sex": "unisexual",
                },
                {
                    "part": "plant",
                    "trait": "part",
                    "start": 59,
                    "end": 65,
                    "sex": "unisexual",
                },
                {
                    "reproduction": "dioecious",
                    "trait": "reproduction",
                    "start": 66,
                    "end": 75,
                    "part": "plant",
                    "sex": "unisexual",
                },
            ],
        )

    def test_descriptor_02(self):
        self.maxDiff = None
        self.assertEqual(
            test("Shrubs , to 1.5 m, forming rhizomatous colonies."),
            [
                {"part": "shrub", "trait": "part", "start": 0, "end": 6},
                {
                    "dimensions": "length",
                    "length_high": 150.0,
                    "part": "shrub",
                    "trait": "size",
                    "start": 9,
                    "end": 17,
                },
            ],
        )

    def test_descriptor_03(self):
        self.assertEqual(
            test("Stems often caespitose"),
            [
                {"part": "stem", "trait": "part", "start": 0, "end": 5},
                {
                    "habit": "cespitose",
                    "trait": "habit",
                    "start": 12,
                    "end": 22,
                },
            ],
        )

    def test_descriptor_04(self):
        self.assertEqual(
            test("Herbs perennial or subshrubs, epiphytic or epilithic."),
            [
                {
                    "woodiness": "herb",
                    "trait": "woodiness",
                    "start": 0,
                    "end": 5,
                    "part": "shrub",
                },
                {
                    "plant_duration": "perennial",
                    "trait": "plant_duration",
                    "start": 6,
                    "end": 15,
                },
                {"part": "shrub", "trait": "part", "start": 19, "end": 28},
                {
                    "habit": "epiphytic",
                    "trait": "habit",
                    "start": 30,
                    "end": 39,
                },
                {
                    "habit": "epilithic",
                    "trait": "habit",
                    "start": 43,
                    "end": 52,
                },
            ],
        )

    def test_descriptor_05(self):
        self.assertEqual(
            test("rosette-trees"),
            [
                {
                    "habit": "rosette-trees",
                    "trait": "habit",
                    "start": 0,
                    "end": 13,
                },
            ],
        )
