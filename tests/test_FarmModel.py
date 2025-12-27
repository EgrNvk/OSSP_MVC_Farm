import unittest
import json
from app.Model.FarmModel import FarmModel

def read_save(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

class TestFarmModel(unittest.TestCase):
    def test_init_balance(self):
        model = FarmModel()
        data=read_save(model.save_file)
        self.assertEqual(model.balance, data.get("balance"), model.balance)

    def test_init_fields_count(self):
        model = FarmModel()
        self.assertEqual(len(model.fields), model.max_fields)

    def test_init_first_fields_unlocked(self):
        model = FarmModel()
        data = read_save(model.save_file)
        saved_fields = data.get("fields")

        if saved_fields:
            for i in range(min(4, len(model.fields), len(saved_fields))):
                expected = saved_fields[i].get("unlocked", True)
                self.assertEqual(model.fields[i].unlocked, expected)
        else:
            for i in range(4):
                self.assertTrue(model.fields[i].unlocked)

    def test_buy_fertilizer_success(self):
        model = FarmModel()
        model.balance = 100

        data_before = read_save(model.save_file)
        before = data_before["warehouse"]["Звичайне добриво (-20%)"]

        result = model.buy_fertilizer("Звичайне добриво (-20%)")

        data_after = read_save(model.save_file)
        after = data_after["warehouse"]["Звичайне добриво (-20%)"]

        self.assertTrue(result)
        self.assertEqual(after, before + 1)

    def test_buy_fertilizer_not_enough_money(self):
        model = FarmModel()
        model.balance = 0

        data_before=read_save(model.save_file)
        before=data_before["warehouse"]["Звичайне добриво (-20%)"]

        result = model.buy_fertilizer("Звичайне добриво (-20%)")

        data_after=read_save(model.save_file)
        after=data_after["warehouse"]["Звичайне добриво (-20%)"]

        self.assertFalse(result)
        self.assertEqual(after, before)

    def test_plant_on_empty_field(self):
        model = FarmModel()

        data_before = read_save(model.save_file)
        saved_fields = data_before.get("fields")

        if saved_fields and len(saved_fields) > 0:
            pass

        result = model.plant_on_field(0, "Пшениця")

        data_after = read_save(model.save_file)

        self.assertTrue(result)
        self.assertEqual(model.fields[0].state, "growing")
        self.assertIn("fields", data_after)
        self.assertEqual(len(data_after["fields"]), len(model.fields))

    def test_plant_on_non_empty_field(self):
        model = FarmModel()
        model.fields[0].state = "growing"

        data_before = read_save(model.save_file)

        result = model.plant_on_field(0, "Пшениця")

        data_after = read_save(model.save_file)

        self.assertFalse(result)
        self.assertEqual(data_after, data_before)

    def test_get_grow_time_positive(self):
        model = FarmModel()

        model.plant_on_field(0, "Пшениця")

        grow_time = model.get_grow_time(0)

        self.assertIsInstance(grow_time, (int, float))
        self.assertGreater(grow_time, 0)

    def test_finish_growth_sets_ready(self):
        model = FarmModel()

        model.fields[0].state = "growing"

        result = model.finish_growth(0)

        if isinstance(result, bool):
            self.assertTrue(result)

        self.assertEqual(model.fields[0].state, "ready")

    def test_harvest_success(self):
        model = FarmModel()

        model.plant_on_field(0, "Пшениця")

        model.fields[0].state = "ready"

        data_before = read_save(model.save_file)
        before = data_before["ambar"].get("Пшениця", 0)

        result = model.harvest(0)

        data_after = read_save(model.save_file)
        after = data_after["ambar"].get("Пшениця", 0)

        if isinstance(result, bool):
            self.assertTrue(result)

        self.assertEqual(after, before + 1)

    def test_sell_success(self):
        model = FarmModel()

        model.ambar["Пшениця"] = 1
        model.balance = 0

        wheat = next(p for p in model.plants if p.name == "Пшениця")
        expected_price = wheat.price

        before_ambar = model.ambar["Пшениця"]
        before_balance = model.balance

        result = model.sell("Пшениця")

        self.assertEqual(result, expected_price)

        self.assertEqual(model.ambar["Пшениця"], before_ambar - 1)

        self.assertEqual(model.balance, before_balance + expected_price)

    def test_sell_fail_when_no_product(self):
        model = FarmModel()

        model.ambar["Пшениця"] = 0
        model.balance = 10

        before_ambar = model.ambar["Пшениця"]
        before_balance = model.balance

        result = model.sell("Пшениця")

        self.assertEqual(result, 0)

        self.assertEqual(model.ambar["Пшениця"], before_ambar)
        self.assertEqual(model.balance, before_balance)
