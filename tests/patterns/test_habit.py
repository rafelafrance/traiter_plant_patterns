import unittest

from tests.setup import test


class TestHabit(unittest.TestCase):
    def test_habit_01(self):
        self.assertEqual(
            test("Stems often caespitose"),
            [
                {"part": "stem", "trait": "part", "start": 0, "end": 5},
                {
                    "plant_habit": "cespitose",
                    "trait": "plant_habit",
                    "start": 12,
                    "end": 22,
                },
            ],
        )

    def test_habit_02(self):
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
                    "plant_habit": "epiphytic",
                    "trait": "plant_habit",
                    "start": 30,
                    "end": 39,
                },
                {
                    "plant_habit": "epilithic",
                    "trait": "plant_habit",
                    "start": 43,
                    "end": 52,
                },
            ],
        )
