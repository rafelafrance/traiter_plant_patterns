import unittest

from tests.setup import test


class TestSize(unittest.TestCase):

    # def test_size_00(self):
    #     test('Leaf (12-)23-34 × 45-56 cm wide')

    def test_size_01(self):
        self.assertEqual(
            test("Leaf (12-)23-34 × 45-56 cm"),
            [
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 4},
                {
                    "dimensions": ["length", "width"],
                    "length_min": 12.0,
                    "length_low": 23.0,
                    "length_high": 34.0,
                    "length_units": "cm",
                    "trait": "size",
                    "start": 5,
                    "end": 26,
                    "width_low": 45.0,
                    "width_high": 56.0,
                    "width_units": "cm",
                    "leaf_part": "leaf",
                },
            ],
        )

    def test_size_02(self):
        self.assertEqual(
            test("leaf (12-)23-34 × 45-56"),
            [{"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 4}],
        )

    def test_size_03(self):
        self.assertEqual(
            test("blade 1.5–5(–7) cm"),
            [
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 5},
                {
                    "dimensions": "length",
                    "length_low": 1.5,
                    "length_high": 5.0,
                    "length_max": 7.0,
                    "length_units": "cm",
                    "trait": "size",
                    "start": 6,
                    "end": 18,
                    "leaf_part": "leaf",
                },
            ],
        )

    def test_size_04(self):
        self.assertEqual(
            test("leaf shallowly to deeply 5–7-lobed"),
            [
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 4},
                {
                    "low": 5,
                    "high": 7,
                    "trait": "count",
                    "start": 25,
                    "end": 34,
                    "leaf_part": "leaf",
                    "subpart": "lobe",
                },
            ],
        )

    def test_size_05(self):
        self.assertEqual(
            test("leaf 4–10 cm wide"),
            [
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 4},
                {
                    "dimensions": "width",
                    "width_low": 4.0,
                    "width_high": 10.0,
                    "width_units": "cm",
                    "trait": "size",
                    "start": 5,
                    "end": 17,
                    "leaf_part": "leaf",
                },
            ],
        )

    def test_size_06(self):
        self.assertEqual(
            test("leaf sinuses 1/5–1/4 to base"),
            [
                {
                    "leaf_part": "leaf",
                    "trait": "leaf_part",
                    "subpart_as_loc": "to base",
                    "start": 0,
                    "end": 4,
                },
                {
                    "subpart": "sinus",
                    "trait": "subpart",
                    "subpart_as_loc": "to base",
                    "start": 5,
                    "end": 12,
                    "leaf_part": "leaf",
                },
                {
                    "subpart_as_loc": "to base",
                    "trait": "subpart_as_loc",
                    "start": 21,
                    "end": 28,
                },
            ],
        )

    def test_size_07(self):
        self.assertEqual(
            test("petiolules 2–5 mm"),
            [
                {"leaf_part": "petiolule", "trait": "leaf_part", "start": 0, "end": 10},
                {
                    "dimensions": "length",
                    "length_low": 2.0,
                    "length_high": 5.0,
                    "length_units": "mm",
                    "trait": "size",
                    "start": 11,
                    "end": 17,
                    "leaf_part": "petiolule",
                },
            ],
        )

    def test_size_08(self):
        self.assertEqual(
            test("petiolules 2–5 mm; coarsely serrate; petioles 16–28 mm."),
            [
                {"leaf_part": "petiolule", "trait": "leaf_part", "start": 0, "end": 10},
                {
                    "dimensions": "length",
                    "length_low": 2.0,
                    "length_high": 5.0,
                    "length_units": "mm",
                    "trait": "size",
                    "start": 11,
                    "end": 17,
                    "leaf_part": "petiolule",
                },
                {
                    "margin": "serrate",
                    "trait": "margin",
                    "start": 19,
                    "end": 35,
                    "leaf_part": "petiolule",
                },
                {"leaf_part": "petiole", "trait": "leaf_part", "start": 37, "end": 45},
                {
                    "dimensions": "length",
                    "length_low": 16.0,
                    "length_high": 28.0,
                    "length_units": "mm",
                    "trait": "size",
                    "start": 46,
                    "end": 55,
                    "leaf_part": "petiole",
                },
            ],
        )

    def test_size_09(self):
        self.assertEqual(
            test("Leaves: petiole 2–15 cm;"),
            [
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 6},
                {"leaf_part": "petiole", "trait": "leaf_part", "start": 8, "end": 15},
                {
                    "dimensions": "length",
                    "length_low": 2.0,
                    "length_high": 15.0,
                    "length_units": "cm",
                    "trait": "size",
                    "start": 16,
                    "end": 23,
                    "leaf_part": "petiole",
                },
            ],
        )

    def test_size_10(self):
        self.assertEqual(
            test("petiole [5–]7–25[–32] mm,"),
            [
                {"leaf_part": "petiole", "trait": "leaf_part", "start": 0, "end": 7},
                {
                    "dimensions": "length",
                    "length_min": 5.0,
                    "length_low": 7.0,
                    "length_high": 25.0,
                    "length_max": 32.0,
                    "length_units": "mm",
                    "trait": "size",
                    "start": 8,
                    "end": 24,
                    "leaf_part": "petiole",
                },
            ],
        )

    def test_size_11(self):
        self.assertEqual(
            test("leaf 2–4 cm × 2–10 mm"),
            [
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 4},
                {
                    "dimensions": ["length", "width"],
                    "length_low": 2.0,
                    "length_high": 4.0,
                    "length_units": "cm",
                    "trait": "size",
                    "start": 5,
                    "end": 21,
                    "leaf_part": "leaf",
                    "width_low": 2.0,
                    "width_high": 10.0,
                    "width_units": "mm",
                },
            ],
        )

    def test_size_12(self):
        self.assertEqual(
            test("leaf deeply to shallowly lobed, 4–5(–7) cm wide,"),
            [
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 4},
                {
                    "subpart": "lobe",
                    "trait": "subpart",
                    "start": 25,
                    "end": 30,
                    "leaf_part": "leaf",
                },
                {
                    "dimensions": "width",
                    "width_low": 4.0,
                    "width_high": 5.0,
                    "width_max": 7.0,
                    "width_units": "cm",
                    "trait": "size",
                    "start": 32,
                    "end": 47,
                    "leaf_part": "leaf",
                },
            ],
        )

    def test_size_13(self):
        self.assertEqual(
            test("""Leaves 3-foliolate,"""),
            [
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 6},
                {
                    "low": 3,
                    "trait": "count",
                    "start": 7,
                    "end": 18,
                    "leaf_part": "leaf",
                    "subpart": "lobe",
                },
            ],
        )

    def test_size_14(self):
        self.assertEqual(
            test("terminal leaflet 3–5 cm, blade petiolule 3–12 mm,"),
            [
                {"location": "terminal", "trait": "location", "start": 0, "end": 8},
                {
                    "leaf_part": "leaflet",
                    "trait": "leaf_part",
                    "start": 9,
                    "end": 16,
                    "location": "terminal",
                },
                {
                    "dimensions": "length",
                    "length_low": 3.0,
                    "length_high": 5.0,
                    "length_units": "cm",
                    "trait": "size",
                    "start": 17,
                    "end": 23,
                    "leaf_part": "leaflet",
                    "location": "terminal",
                },
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 25, "end": 30},
                {
                    "leaf_part": "petiolule",
                    "trait": "leaf_part",
                    "start": 31,
                    "end": 40,
                },
                {
                    "dimensions": "length",
                    "length_low": 3.0,
                    "length_high": 12.0,
                    "length_units": "mm",
                    "trait": "size",
                    "start": 41,
                    "end": 48,
                    "leaf_part": "petiolule",
                },
            ],
        )

    def test_size_15(self):
        self.assertEqual(
            test("leaf shallowly 3–5(–7)-lobed, 5–25 × (8–)10–25(–30) cm,"),
            [
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 4},
                {
                    "low": 3,
                    "high": 5,
                    "max": 7,
                    "trait": "count",
                    "start": 15,
                    "end": 28,
                    "subpart": "lobe",
                    "leaf_part": "leaf",
                },
                {
                    "dimensions": ["length", "width"],
                    "length_low": 5.0,
                    "length_high": 25.0,
                    "length_units": "cm",
                    "width_min": 8.0,
                    "width_low": 10.0,
                    "width_high": 25.0,
                    "width_max": 30.0,
                    "width_units": "cm",
                    "trait": "size",
                    "start": 30,
                    "end": 54,
                    "leaf_part": "leaf",
                },
            ],
        )

    def test_size_16(self):
        self.assertEqual(
            test("(3–)5-lobed, 6–20(–30) × 6–25 cm,"),
            [
                {
                    "min": 3,
                    "low": 5,
                    "trait": "count",
                    "start": 0,
                    "end": 11,
                    "subpart": "lobe",
                },
                {
                    "dimensions": ["length", "width"],
                    "length_low": 6.0,
                    "length_high": 20.0,
                    "length_max": 30.0,
                    "length_units": "cm",
                    "trait": "size",
                    "start": 13,
                    "end": 32,
                    "width_low": 6.0,
                    "width_high": 25.0,
                    "width_units": "cm",
                },
            ],
        )

    def test_size_17(self):
        self.assertEqual(
            test("petiole to 11 cm;"),
            [
                {"leaf_part": "petiole", "trait": "leaf_part", "start": 0, "end": 7},
                {
                    "dimensions": "length",
                    "length_high": 11.0,
                    "length_units": "cm",
                    "trait": "size",
                    "start": 8,
                    "end": 16,
                    "leaf_part": "petiole",
                },
            ],
        )

    def test_size_18(self):
        self.assertEqual(
            test("petals (1–)3–10(–12) mm (pistillate) or 5–8(–10) mm (staminate)"),
            [
                {
                    "flower_part": "petal",
                    "trait": "flower_part",
                    "start": 0,
                    "end": 6,
                },
                {
                    "dimensions": "length",
                    "length_min": 1.0,
                    "length_low": 3.0,
                    "length_high": 10.0,
                    "length_max": 12.0,
                    "length_units": "mm",
                    "sex": "pistillate",
                    "trait": "size",
                    "start": 7,
                    "end": 36,
                    "flower_part": "petal",
                },
                {
                    "dimensions": "length",
                    "length_low": 5.0,
                    "length_high": 8.0,
                    "length_max": 10.0,
                    "length_units": "mm",
                    "sex": "staminate",
                    "trait": "size",
                    "start": 40,
                    "end": 63,
                    "flower_part": "petal",
                },
            ],
        )

    def test_size_19(self):
        self.assertEqual(
            test("Flowers 5–10 cm diam.; hypanthium 4–8 mm,"),
            [
                {"flower_part": "flower", "trait": "flower_part", "start": 0, "end": 7},
                {
                    "dimensions": "diameter",
                    "diameter_low": 5.0,
                    "diameter_high": 10.0,
                    "diameter_units": "cm",
                    "trait": "size",
                    "start": 8,
                    "end": 21,
                    "flower_part": "flower",
                },
                {
                    "flower_part": "hypanthium",
                    "trait": "flower_part",
                    "start": 23,
                    "end": 33,
                },
                {
                    "dimensions": "length",
                    "length_low": 4.0,
                    "length_high": 8.0,
                    "length_units": "mm",
                    "trait": "size",
                    "start": 34,
                    "end": 40,
                    "flower_part": "hypanthium",
                },
            ],
        )

    def test_size_20(self):
        self.assertEqual(
            test("Flowers 5--16 × 4--12 cm"),
            [
                {"flower_part": "flower", "trait": "flower_part", "start": 0, "end": 7},
                {
                    "dimensions": ["length", "width"],
                    "length_low": 5.0,
                    "length_high": 16.0,
                    "length_units": "cm",
                    "trait": "size",
                    "start": 8,
                    "end": 24,
                    "flower_part": "flower",
                    "width_low": 4.0,
                    "width_high": 12.0,
                    "width_units": "cm",
                },
            ],
        )

    def test_size_21(self):
        self.assertEqual(
            test(
                """
                Inflorescences formed season before flowering and exposed
                during winter; staminate catkins 3--8.5 cm,"""
            ),
            [
                {
                    "inflorescence": "inflorescence",
                    "trait": "inflorescence",
                    "start": 0,
                    "end": 14,
                },
                {"sex": "staminate", "trait": "sex", "start": 73, "end": 82},
                {
                    "inflorescence": "catkin",
                    "trait": "inflorescence",
                    "start": 83,
                    "end": 90,
                    "sex": "staminate",
                },
                {
                    "dimensions": "length",
                    "length_low": 3.0,
                    "length_high": 8.5,
                    "length_units": "cm",
                    "trait": "size",
                    "start": 91,
                    "end": 100,
                    "inflorescence": "catkin",
                    "sex": "staminate",
                },
            ],
        )

    def test_size_22(self):
        self.assertEqual(
            test("Leaflets petiolulate; blade ovate, 8-15 × 4-15 cm,"),
            [
                {"leaf_part": "leaflet", "trait": "leaf_part", "start": 0, "end": 8},
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 22, "end": 27},
                {
                    "shape": "ovate",
                    "trait": "shape",
                    "start": 28,
                    "end": 33,
                    "leaf_part": "leaf",
                },
                {
                    "dimensions": ["length", "width"],
                    "length_low": 8.0,
                    "length_high": 15.0,
                    "length_units": "cm",
                    "trait": "size",
                    "start": 35,
                    "end": 49,
                    "leaf_part": "leaf",
                    "width_low": 4.0,
                    "width_high": 15.0,
                    "width_units": "cm",
                },
            ],
        )

    def test_size_23(self):
        self.assertEqual(
            test("calyx, 8-10 mm, 3-4 mm high,"),
            [
                {"flower_part": "calyx", "trait": "flower_part", "start": 0, "end": 5},
                {
                    "dimensions": ["height", "length"],
                    "length_low": 8.0,
                    "length_high": 10.0,
                    "length_units": "mm",
                    "height_low": 3.0,
                    "height_high": 4.0,
                    "height_units": "mm",
                    "trait": "size",
                    "start": 7,
                    "end": 27,
                    "flower_part": "calyx",
                },
            ],
        )

    def test_size_24(self):
        self.assertEqual(
            test("Petals 15-21 × ca. 8 mm,"),
            [
                {"flower_part": "petal", "trait": "flower_part", "start": 0, "end": 6},
                {
                    "dimensions": ["length", "width"],
                    "length_low": 15.0,
                    "length_high": 21.0,
                    "length_units": "mm",
                    "trait": "size",
                    "start": 7,
                    "end": 23,
                    "flower_part": "petal",
                    "width_low": 8.0,
                    "width_units": "mm",
                    "uncertain": True,
                },
            ],
        )

    def test_size_25(self):
        self.assertEqual(
            test("Petals ca 8 mm."),
            [
                {"flower_part": "petal", "trait": "flower_part", "start": 0, "end": 6},
                {
                    "dimensions": "length",
                    "length_low": 8.0,
                    "length_units": "mm",
                    "trait": "size",
                    "start": 7,
                    "end": 15,
                    "flower_part": "petal",
                    "uncertain": True,
                },
            ],
        )

    def test_size_26(self):
        self.assertEqual(
            test("Legumes 7-10 mm, 2.8-4.5 mm high and wide"),
            [
                {"fruit_part": "legume", "trait": "fruit_part", "start": 0, "end": 7},
                {
                    "dimensions": ["height", "width"],
                    "height_low": 7.0,
                    "height_high": 10.0,
                    "trait": "size",
                    "start": 8,
                    "end": 41,
                    "fruit_part": "legume",
                    "width_low": 2.8,
                    "width_high": 4.5,
                },
            ],
        )

    def test_size_27(self):
        self.assertEqual(
            test("Racemes 3-4 cm,"),
            [
                {
                    "inflorescence": "raceme",
                    "trait": "inflorescence",
                    "start": 0,
                    "end": 7,
                },
                {
                    "dimensions": "length",
                    "length_low": 3.0,
                    "length_high": 4.0,
                    "length_units": "cm",
                    "trait": "size",
                    "start": 8,
                    "end": 14,
                    "inflorescence": "raceme",
                },
            ],
        )

    def test_size_28(self):
        self.assertEqual(
            test("Petals pale violet, with darker keel; standard elliptic, 6-7 × 3-4;"),
            [
                {"flower_part": "petal", "trait": "flower_part", "start": 0, "end": 6},
                {
                    "color": "purple",
                    "trait": "color",
                    "start": 7,
                    "end": 18,
                    "flower_part": "petal",
                },
                {
                    "flower_part": "keel",
                    "trait": "flower_part",
                    "start": 32,
                    "end": 36,
                },
                {
                    "shape": "elliptic",
                    "trait": "shape",
                    "start": 47,
                    "end": 55,
                    "flower_part": "keel",
                },
            ],
        )

    def test_size_29(self):
        self.assertEqual(
            test("Seeds ca. 1.6 × 1-1.3 × 0.7-0.8 cm; hilum 8-10 mm."),
            [
                {"fruit_part": "seed", "trait": "fruit_part", "start": 0, "end": 5},
                {
                    "dimensions": ["length", "thickness", "width"],
                    "length_low": 1.6,
                    "length_units": "cm",
                    "width_low": 1.0,
                    "width_high": 1.3,
                    "width_units": "cm",
                    "thickness_low": 0.7,
                    "thickness_high": 0.8,
                    "thickness_units": "cm",
                    "trait": "size",
                    "start": 6,
                    "end": 34,
                    "uncertain": True,
                    "fruit_part": "seed",
                },
                {"fruit_part": "hilum", "trait": "fruit_part", "start": 36, "end": 41},
                {
                    "dimensions": "length",
                    "length_low": 8.0,
                    "length_high": 10.0,
                    "length_units": "mm",
                    "trait": "size",
                    "start": 42,
                    "end": 50,
                    "fruit_part": "hilum",
                },
            ],
        )

    def test_size_30(self):
        self.assertEqual(
            test("leaflets obovate, 1-2.5 × to 1.6 cm,"),
            [
                {"leaf_part": "leaflet", "trait": "leaf_part", "start": 0, "end": 8},
                {
                    "shape": "obovate",
                    "trait": "shape",
                    "start": 9,
                    "end": 16,
                    "leaf_part": "leaflet",
                },
                {
                    "dimensions": ["length", "width"],
                    "length_low": 1.0,
                    "length_high": 2.5,
                    "length_units": "cm",
                    "trait": "size",
                    "start": 18,
                    "end": 35,
                    "leaf_part": "leaflet",
                    "width_low": 1.6,
                    "width_units": "cm",
                },
            ],
        )

    def test_size_31(self):
        self.assertEqual(
            test("Shrubs, 0.5–1[–2.5] m."),
            [
                {"part": "shrub", "trait": "part", "start": 0, "end": 6},
                {
                    "dimensions": "length",
                    "length_low": 0.5,
                    "length_high": 1.0,
                    "length_max": 2.5,
                    "length_units": "m",
                    "trait": "size",
                    "part": "shrub",
                    "start": 8,
                    "end": 22,
                },
            ],
        )

    def test_size_32(self):
        self.assertEqual(
            test("trunk to 3(?) cm d.b.h.;"),
            [
                {"part": "trunk", "trait": "part", "start": 0, "end": 5},
                {
                    "dimensions": "dbh",
                    "dbh_high": 3.0,
                    "dbh_units": "cm",
                    "uncertain": True,
                    "trait": "size",
                    "start": 6,
                    "end": 23,
                    "part": "trunk",
                },
            ],
        )

    def test_size_33(self):
        self.assertEqual(
            test("Trees to 25 m tall; bark yellow-brown, fissured."),
            [
                {"part": "tree", "trait": "part", "start": 0, "end": 5},
                {
                    "dimensions": "height",
                    "height_high": 25.0,
                    "height_units": "m",
                    "trait": "size",
                    "start": 6,
                    "end": 18,
                    "part": "tree",
                },
                {"part": "bark", "trait": "part", "start": 20, "end": 24},
                {
                    "color": "yellow-brown",
                    "trait": "color",
                    "start": 25,
                    "end": 37,
                    "part": "bark",
                },
            ],
        )

    def test_size_34(self):
        self.assertEqual(
            test("Shrubs or trees , 3-50 m. Bark light to dark gray"),
            [
                {"part": "shrub", "trait": "part", "start": 0, "end": 6},
                {"part": "tree", "trait": "part", "start": 10, "end": 15},
                {
                    "dimensions": "length",
                    "length_low": 3.0,
                    "length_high": 50.0,
                    "length_units": "m",
                    "trait": "size",
                    "start": 18,
                    "end": 25,
                    "part": "tree",
                },
                {"part": "bark", "trait": "part", "start": 26, "end": 30},
                {
                    "color": "gray",
                    "trait": "color",
                    "start": 40,
                    "end": 49,
                    "part": "bark",
                },
            ],
        )

    def test_size_35(self):
        self.assertEqual(
            test("Leaves (2-)3-5 mm ."),
            [
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 6},
                {
                    "dimensions": "length",
                    "length_min": 2.0,
                    "length_low": 3.0,
                    "length_high": 5.0,
                    "length_units": "mm",
                    "trait": "size",
                    "start": 7,
                    "end": 19,
                    "leaf_part": "leaf",
                },
            ],
        )

    def test_size_36(self):
        self.assertEqual(
            test("articles ±4.5 mm long;"),
            [
                {"subpart": "article", "trait": "subpart", "start": 0, "end": 8},
                {
                    "dimensions": "length",
                    "length_low": 4.5,
                    "length_units": "mm",
                    "trait": "size",
                    "start": 9,
                    "end": 21,
                    "uncertain": True,
                    "subpart": "article",
                },
            ],
        )

    def test_size_37(self):
        self.assertEqual(
            test("seeds ± 4 x 3 mm."),
            [
                {"fruit_part": "seed", "trait": "fruit_part", "start": 0, "end": 5},
                {
                    "dimensions": ["length", "width"],
                    "length_low": 4.0,
                    "length_units": "mm",
                    "width_low": 3.0,
                    "width_units": "mm",
                    "trait": "size",
                    "start": 6,
                    "end": 17,
                    "uncertain": True,
                    "fruit_part": "seed",
                },
            ],
        )

    def test_size_38(self):
        self.assertEqual(
            test("coastal plain to 1500 m,"),
            [{"shape": "plain", "trait": "shape", "start": 8, "end": 13}],
        )

    def test_size_39(self):
        self.assertEqual(
            test("trunk to 8(-?) cm diam."),
            [
                {"part": "trunk", "trait": "part", "start": 0, "end": 5},
                {
                    "dimensions": "diameter",
                    "diameter_low": 8.0,
                    "diameter_units": "cm",
                    "trait": "size",
                    "start": 9,
                    "end": 23,
                    "part": "trunk",
                },
            ],
        )

    def test_size_40(self):
        self.assertEqual(
            test(
                """setae to 2-6 mm and to 0.4-0.7 mm diam. at base, these mixed with
                non-secretory setulae"""
            ),
            [
                {"part": "setae", "trait": "part", "start": 0, "end": 5},
                {
                    "length_low": 2.0,
                    "length_high": 6.0,
                    "length_units": "mm",
                    "dimensions": "length",
                    "trait": "size",
                    "start": 9,
                    "end": 15,
                    "part": "setae",
                },
                {
                    "diameter_low": 0.4,
                    "diameter_high": 0.7,
                    "diameter_units": "mm",
                    "dimensions": "diameter",
                    "trait": "size",
                    "start": 23,
                    "end": 39,
                    "part": "setae",
                    "subpart_as_loc": "at base",
                },
                {
                    "subpart_as_loc": "at base",
                    "trait": "subpart_as_loc",
                    "start": 40,
                    "end": 47,
                },
                {"part": "setulae", "trait": "part", "start": 80, "end": 87},
            ],
        )

    def test_size_41(self):
        self.assertEqual(
            test("""setae (3.5-)4-7 x (1.5_)2- 2.8 mm"""),
            [
                {"part": "setae", "trait": "part", "start": 0, "end": 5},
                {
                    "length_min": 3.5,
                    "length_low": 4.0,
                    "length_high": 7.0,
                    "length_units": "mm",
                    "dimensions": ["length", "width"],
                    "width_min": 1.5,
                    "width_low": 2.0,
                    "width_high": 2.8,
                    "width_units": "mm",
                    "trait": "size",
                    "start": 6,
                    "end": 33,
                    "part": "setae",
                },
            ],
        )
