import unittest
from app.Model.FarmModel import FarmModel

class TestFarmModel(unittest.TestCase):
    def test_init_balance(self):
        model = FarmModel()
        self.assertEqual(model.balance, 50)

    def test_init_fields_count(self):
        model = FarmModel()
        self.assertEqual(len(model.fields), model.max_fields)

    def test_init_first_fields_unlocked(self):
        model = FarmModel()
        for i in range(4):
            self.assertTrue(model.fields[i].unlocked)
