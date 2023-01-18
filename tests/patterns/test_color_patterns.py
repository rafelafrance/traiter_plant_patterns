import unittest

from tests.setup import test


class TestColor(unittest.TestCase):
    def test_color_01(self):
        self.assertEqual(
            test(
                """hypanthium green or greenish yellow,
                usually not purple-spotted, rarely purple-spotted distally.
                """
            ),
            [
                {
                    "flower_part": "hypanthium",
                    "trait": "flower_part",
                    "start": 0,
                    "end": 10,
                },
                {
                    "color": "green",
                    "trait": "color",
                    "start": 11,
                    "end": 16,
                    "flower_part": "hypanthium",
                },
                {
                    "color": "green-yellow",
                    "trait": "color",
                    "start": 20,
                    "end": 35,
                    "flower_part": "hypanthium",
                },
                {
                    "color": "purple-spotted",
                    "missing": True,
                    "trait": "color",
                    "start": 45,
                    "end": 63,
                    "flower_part": "hypanthium",
                },
                {
                    "color": "purple-spotted",
                    "missing": True,
                    "trait": "color",
                    "start": 65,
                    "end": 86,
                    "flower_part": "hypanthium",
                    "location": "distal",
                },
                {"location": "distal", "trait": "location", "start": 87, "end": 95},
            ],
        )

    def test_color_02(self):
        self.assertEqual(
            test("hypanthium straw-colored to sulphur-yellow or golden-yellow."),
            [
                {
                    "flower_part": "hypanthium",
                    "trait": "flower_part",
                    "start": 0,
                    "end": 10,
                },
                {
                    "color": "yellow",
                    "trait": "color",
                    "flower_part": "hypanthium",
                    "start": 11,
                    "end": 24,
                },
                {
                    "color": "yellow",
                    "trait": "color",
                    "flower_part": "hypanthium",
                    "start": 28,
                    "end": 42,
                },
                {
                    "color": "yellow",
                    "trait": "color",
                    "flower_part": "hypanthium",
                    "start": 46,
                    "end": 59,
                },
            ],
        )

    def test_color_03(self):
        self.assertEqual(
            test("sepals erect, green- or red-tipped."),
            [
                {"flower_part": "sepal", "trait": "flower_part", "start": 0, "end": 6},
                {
                    "color": "green",
                    "trait": "color",
                    "flower_part": "sepal",
                    "start": 14,
                    "end": 20,
                },
                {
                    "color": "red-tipped",
                    "trait": "color",
                    "flower_part": "sepal",
                    "start": 24,
                    "end": 34,
                },
            ],
        )

    def test_color_04(self):
        self.assertEqual(
            test("petals white, cream, or pale green [orange to yellow]."),
            [
                {"flower_part": "petal", "trait": "flower_part", "start": 0, "end": 6},
                {
                    "color": "white",
                    "trait": "color",
                    "flower_part": "petal",
                    "start": 7,
                    "end": 12,
                },
                {
                    "color": "white",
                    "trait": "color",
                    "flower_part": "petal",
                    "start": 14,
                    "end": 19,
                },
                {
                    "color": "green",
                    "trait": "color",
                    "flower_part": "petal",
                    "start": 24,
                    "end": 34,
                },
                {
                    "color": "orange",
                    "trait": "color",
                    "flower_part": "petal",
                    "start": 36,
                    "end": 42,
                },
                {
                    "color": "yellow",
                    "trait": "color",
                    "flower_part": "petal",
                    "start": 46,
                    "end": 52,
                },
            ],
        )

    def test_color_05(self):
        """It handles pattern notations within colors."""
        self.maxDiff = None
        self.assertEqual(
            test(
                """
                petals distinct, white to cream, greenish yellow,
                maturing yellowish or pale brown, commonly mottled or with
                light green or white longitudinal stripes.
                """
            ),
            [
                {"flower_part": "petal", "trait": "flower_part", "start": 0, "end": 6},
                {
                    "color": "white",
                    "trait": "color",
                    "flower_part": "petal",
                    "start": 17,
                    "end": 22,
                },
                {
                    "color": "white",
                    "trait": "color",
                    "flower_part": "petal",
                    "start": 26,
                    "end": 31,
                },
                {
                    "color": "green-yellow",
                    "trait": "color",
                    "flower_part": "petal",
                    "start": 33,
                    "end": 48,
                },
                {
                    "color": "yellow",
                    "trait": "color",
                    "flower_part": "petal",
                    "start": 59,
                    "end": 68,
                },
                {
                    "color": "brown",
                    "trait": "color",
                    "flower_part": "petal",
                    "start": 72,
                    "end": 82,
                },
                {
                    "color": "green",
                    "trait": "color",
                    "flower_part": "petal",
                    "start": 109,
                    "end": 120,
                },
                {
                    "color": "white-longitudinal-stripes",
                    "trait": "color",
                    "flower_part": "petal",
                    "start": 124,
                    "end": 150,
                },
            ],
        )

    def test_color_06(self):
        self.assertEqual(
            test(
                """
                Petals distinct, white to cream, greenish white,
                or yellowish green, or yellowish, usually green-throated
                and faintly green-lined.
                """
            ),
            [
                {"flower_part": "petal", "trait": "flower_part", "start": 0, "end": 6},
                {
                    "color": "white",
                    "trait": "color",
                    "flower_part": "petal",
                    "start": 17,
                    "end": 22,
                },
                {
                    "color": "white",
                    "trait": "color",
                    "flower_part": "petal",
                    "start": 26,
                    "end": 31,
                },
                {
                    "color": "green-white",
                    "trait": "color",
                    "flower_part": "petal",
                    "start": 33,
                    "end": 47,
                },
                {
                    "color": "yellow-green",
                    "trait": "color",
                    "flower_part": "petal",
                    "start": 52,
                    "end": 67,
                },
                {
                    "color": "yellow",
                    "trait": "color",
                    "flower_part": "petal",
                    "start": 72,
                    "end": 81,
                },
                {
                    "color": "green-throated",
                    "trait": "color",
                    "flower_part": "petal",
                    "start": 91,
                    "end": 105,
                },
                {
                    "color": "green-lined",
                    "trait": "color",
                    "flower_part": "petal",
                    "start": 110,
                    "end": 129,
                },
            ],
        )

    def test_color_07(self):
        self.assertEqual(
            test("calyx yellow"),
            [
                {"flower_part": "calyx", "trait": "flower_part", "start": 0, "end": 5},
                {
                    "color": "yellow",
                    "trait": "color",
                    "flower_part": "calyx",
                    "start": 6,
                    "end": 12,
                },
            ],
        )

    def test_color_08(self):
        self.assertEqual(
            test("corolla yellow"),
            [
                {
                    "flower_part": "corolla",
                    "trait": "flower_part",
                    "start": 0,
                    "end": 7,
                },
                {
                    "color": "yellow",
                    "trait": "color",
                    "flower_part": "corolla",
                    "start": 8,
                    "end": 14,
                },
            ],
        )

    def test_color_09(self):
        self.assertEqual(
            test("flower yellow"),
            [
                {"flower_part": "flower", "trait": "flower_part", "start": 0, "end": 6},
                {
                    "color": "yellow",
                    "trait": "color",
                    "flower_part": "flower",
                    "start": 7,
                    "end": 13,
                },
            ],
        )

    def test_color_10(self):
        self.assertEqual(
            test("hypanthium yellow"),
            [
                {
                    "flower_part": "hypanthium",
                    "trait": "flower_part",
                    "start": 0,
                    "end": 10,
                },
                {
                    "color": "yellow",
                    "trait": "color",
                    "flower_part": "hypanthium",
                    "start": 11,
                    "end": 17,
                },
            ],
        )

    def test_color_11(self):
        self.assertEqual(
            test("petal pale sulfur-yellow."),
            [
                {"flower_part": "petal", "trait": "flower_part", "start": 0, "end": 5},
                {
                    "color": "yellow",
                    "trait": "color",
                    "flower_part": "petal",
                    "start": 6,
                    "end": 24,
                },
            ],
        )

    def test_color_12(self):
        self.assertEqual(
            test("sepal yellow"),
            [
                {"flower_part": "sepal", "trait": "flower_part", "start": 0, "end": 5},
                {
                    "color": "yellow",
                    "trait": "color",
                    "flower_part": "sepal",
                    "start": 6,
                    "end": 12,
                },
            ],
        )

    def test_color_13(self):
        self.assertEqual(
            test("Leaves acaulescent or nearly so, with white hairs."),
            [
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 6},
                {
                    "habit": "acaulescent",
                    "trait": "habit",
                    "start": 7,
                    "end": 18,
                },
                {
                    "color": "white",
                    "trait": "color",
                    "leaf_part": "leaf",
                    "subpart": "hair",
                    "start": 38,
                    "end": 43,
                },
                {
                    "subpart": "hair",
                    "leaf_part": "leaf",
                    "trait": "subpart",
                    "start": 44,
                    "end": 49,
                },
            ],
        )

    def test_color_14(self):
        self.assertEqual(
            test("leaflets surfaces rather densely spotted with blackish dots"),
            [
                {"leaf_part": "leaflet", "trait": "leaf_part", "start": 0, "end": 8},
                {
                    "surface": "surface",
                    "trait": "surface",
                    "start": 9,
                    "end": 17,
                    "leaf_part": "leaflet",
                },
                {
                    "color": "black-dots",
                    "trait": "color",
                    "start": 46,
                    "end": 59,
                    "leaf_part": "leaflet",
                },
            ],
        )

    def test_color_15(self):
        self.assertEqual(
            test("Petals purplish in life, whitish yellowish when dry;"),
            [
                {"flower_part": "petal", "trait": "flower_part", "start": 0, "end": 6},
                {
                    "color": "purple",
                    "trait": "color",
                    "flower_part": "petal",
                    "start": 7,
                    "end": 15,
                },
                {
                    "color": "white-yellow",
                    "trait": "color",
                    "flower_part": "petal",
                    "start": 25,
                    "end": 42,
                },
            ],
        )

    def test_color_16(self):
        self.assertEqual(
            test("Petals red or golden yellowish"),
            [
                {"flower_part": "petal", "trait": "flower_part", "start": 0, "end": 6},
                {
                    "color": "red",
                    "trait": "color",
                    "flower_part": "petal",
                    "start": 7,
                    "end": 10,
                },
                {
                    "color": "yellow",
                    "trait": "color",
                    "flower_part": "petal",
                    "start": 14,
                    "end": 30,
                },
            ],
        )

    def test_color_17(self):
        self.assertEqual(
            test("twigs: young growth green or reddish-tinged."),
            [
                {"part": "twig", "trait": "part", "start": 0, "end": 5},
                {
                    "color": "green",
                    "trait": "color",
                    "part": "twig",
                    "start": 20,
                    "end": 25,
                },
                {
                    "color": "red-tinged",
                    "trait": "color",
                    "part": "twig",
                    "start": 29,
                    "end": 43,
                },
            ],
        )

    def test_color_18(self):
        self.assertEqual(
            test("ex Britton & Rose, N. Amer. R ."),
            [],
        )

    def test_color_19(self):
        self.assertEqual(
            test(
                """stipules, the young stems and lf-axes hispid with stout, partly
                confluent or branched, yellowish setae"""
            ),
            [
                {"leaf_part": "stipule", "trait": "leaf_part", "start": 0, "end": 8},
                {
                    "multiple_parts": ["stem", "leaf-axis"],
                    "trait": "multiple_parts",
                    "start": 20,
                    "end": 37,
                },
                {
                    "surface": "hispid",
                    "trait": "surface",
                    "start": 38,
                    "end": 44,
                    "multiple_parts": ["stem", "leaf-axis"],
                },
                {
                    "shape": "confluent",
                    "trait": "shape",
                    "start": 57,
                    "end": 73,
                    "part": "setae",
                },
                {
                    "shape": "branched",
                    "trait": "shape",
                    "start": 77,
                    "end": 85,
                    "part": "setae",
                },
                {
                    "color": "yellow",
                    "trait": "color",
                    "start": 87,
                    "end": 96,
                    "part": "setae",
                },
                {"part": "setae", "trait": "part", "start": 97, "end": 102},
            ],
        )
