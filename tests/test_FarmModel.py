import unittest
from app.Model.FarmModel import FarmModel

class TestFarmModel(unittest.TestCase):
    def test_init_balance(self):
        model = FarmModel()
        self.assertEqual(model.balance, 90)

    def test_init_fields_count(self):
        model = FarmModel()
        self.assertEqual(len(model.fields), model.max_fields)

    def test_init_first_fields_unlocked(self):
        model = FarmModel()
        for i in range(4):
            self.assertTrue(model.fields[i].unlocked)

    def test_buy_fertilizer_success(self):
        model = FarmModel()
        model.balance = 100

        result = model.buy_fertilizer("Звичайне добриво (-20%)")

        self.assertTrue(result)
        self.assertEqual(model.warehouse["Звичайне добриво (-20%)"], 3)

    def test_buy_fertilizer_not_enough_money(self):
        model = FarmModel()
        model.balance = 0

        result = model.buy_fertilizer("Звичайне добриво (-20%)")

        self.assertFalse(result)

    def test_plant_on_empty_field(self):
        model = FarmModel()

        result = model.plant_on_field(0, "Пшениця")

        self.assertTrue(result)
        self.assertEqual(model.fields[0].state, "growing")

    def test_plant_on_non_empty_field(self):
        model = FarmModel()
        model.fields[0].state = "growing"

        result = model.plant_on_field(0, "Пшениця")

        self.assertFalse(result)