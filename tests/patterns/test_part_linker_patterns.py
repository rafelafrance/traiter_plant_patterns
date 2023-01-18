import unittest

from tests.setup import test


class TestPartLinker(unittest.TestCase):
    def test_part_linker_01(self):
        self.assertEqual(
            test("""pinnules up to 31 pairs,"""),
            [
                {"leaf_part": "pinnule", "trait": "leaf_part", "start": 0, "end": 8},
                {
                    "low": 31,
                    "trait": "count",
                    "start": 15,
                    "end": 23,
                    "count_group": "pairs",
                    "leaf_part": "pinnule",
                },
            ],
        )

    def test_part_linker_02(self):
        self.assertEqual(
            test(
                """trees closely resembling another thing in habit,
                attaining 2-4 m in height with trunk"""
            ),
            [
                {"part": "tree", "trait": "part", "start": 0, "end": 5},
                {
                    "dimensions": "height",
                    "height_low": 2.0,
                    "height_high": 4.0,
                    "height_units": "m",
                    "trait": "size",
                    "start": 59,
                    "end": 74,
                    "part": "tree",
                },
                {"part": "trunk", "trait": "part", "start": 80, "end": 85},
            ],
        )

    def test_part_linker_03(self):
        self.assertEqual(
            test(
                """Pods here are some words, and more words, we keep writing things
                 until the desired part is far away from its size 25-35 X 12-18 mm,
                 the replum 1.5-2 mm wide,"""
            ),
            [
                {"fruit_part": "pod", "trait": "fruit_part", "start": 0, "end": 4},
                {
                    "dimensions": ["length", "width"],
                    "length_low": 25.0,
                    "length_high": 35.0,
                    "length_units": "mm",
                    "width_low": 12.0,
                    "width_high": 18.0,
                    "width_units": "mm",
                    "trait": "size",
                    "start": 114,
                    "end": 130,
                    "fruit_part": "pod",
                },
                {
                    "fruit_part": "replum",
                    "trait": "fruit_part",
                    "start": 136,
                    "end": 142,
                },
                {
                    "dimensions": "width",
                    "width_low": 1.5,
                    "width_high": 2.0,
                    "width_units": "mm",
                    "trait": "size",
                    "start": 143,
                    "end": 156,
                    "fruit_part": "replum",
                },
            ],
        )

    def test_part_linker_04(self):
        self.assertEqual(
            test(
                """Lvs (except of Af. pachyphloia) bipinnate, the primary and secondary
                axes normally pulvinate (the primary pulvinus rarely suppressed)"""
            ),
            [
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 3},
                {
                    "level": "species",
                    "taxon": "Af. pachyphloia",
                    "trait": "taxon",
                    "start": 15,
                    "end": 30,
                },
                {
                    "venation": "bipinnate",
                    "trait": "venation",
                    "start": 32,
                    "end": 41,
                    "leaf_part": "leaf",
                },
                {
                    "subpart": "axis",
                    "trait": "subpart",
                    "start": 69,
                    "end": 73,
                    "part": "primary pulvinus",
                },
                {
                    "shape": "pulvinate",
                    "trait": "shape",
                    "start": 83,
                    "end": 92,
                    "part": "primary pulvinus",
                    "subpart": "axis",
                },
                {"trait": "part", "start": 98, "end": 114, "part": "primary pulvinus"},
            ],
        )
