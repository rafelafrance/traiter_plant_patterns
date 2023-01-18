# import unittest
# from tests.setup import test
# class TestTaxonLinker(unittest.TestCase):
#     def test_taxon_linker_01(self):
#         self.assertEqual(
#             test(
#                 """ser. Glanduliferae, in which a petiolar nectary and ovate
#                     anthers,"""
#             ),
#             [
#                 {
#                     "level": "series",
#                     "taxon": "ser. Glanduliferae",
#                     "trait": "taxon",
#                     "start": 0,
#                     "end": 18,
#                 },
#                 {
#                     "location": "petiolar",
#                     "trait": "location",
#                     "start": 31,
#                     "end": 39,
#                     "taxon": "ser. Glanduliferae",
#                 },
#                 {
#                     "flower_part": "nectary",
#                     "trait": "flower_part",
#                     "start": 40,
#                     "end": 47,
#                     "location": "petiolar",
#                     "taxon": "ser. Glanduliferae",
#                 },
#                 {
#                     "shape": "ovate",
#                     "trait": "shape",
#                     "start": 52,
#                     "end": 57,
#                     "male_flower_part": "anther",
#                     "flower_part": "nectary",
#                     "taxon": "ser. Glanduliferae",
#                 },
#                 {
#                     "male_flower_part": "anther",
#                     "trait": "male_flower_part",
#                     "start": 58,
#                     "end": 65,
#                     "location": "petiolar",
#                     "taxon": "ser. Glanduliferae",
#                 },
#             ],
#         )
#     def test_taxon_linker_02(self):
#         self.assertEqual(
#             test(
#                 """Mimosa sensitiva is one of a sympatric pair of arborescent
#                     mimosas"""
#             ),
#             [
#                 {
#                     "level": "species",
#                     "taxon": "Mimosa sensitiva",
#                     "trait": "taxon",
#                     "start": 0,
#                     "end": 16,
#                 },
#                 {
#                     "trait": "habit",
#                     "start": 47,
#                     "end": 58,
#                     "habit": "arborescent",
#                     "taxon": "Mimosa sensitiva",
#                 },
#             ],
#         )
