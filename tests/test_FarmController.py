import unittest
import time
import threading

import app.Controller.FarmController as FCmod




def dummy(*args, **kwargs):
    pass


class DummyVar:
    def __init__(self, value):
        self._value = value

    def get(self):
        return self._value

    def set(self, value):
        self._value = value


class DummyRoot:
    def __init__(self):
        self.after_calls = []

    def after(self, ms, func):
        self.after_calls.append((ms, func))
        func()




class Field:
    def __init__(self, unlocked=True, state="empty"):
        self.unlocked = unlocked
        self.state = state
        self.bonus = None


class Fertilizer:
    def __init__(self, name, price):
        self.name = name
        self.price = price


class SpyMissionsController:
    def __init__(self, model):
        self.model = model
        self.calls = []

    def sync_all(self):
        self.calls.append(("sync_all", None))

    def after_field_unlocked(self):
        self.calls.append(("after_field_unlocked", None))

    def after_balance_change(self):
        self.calls.append(("after_balance_change", None))

    def after_plant(self, fertilizer_used=False):
        self.calls.append(("after_plant", fertilizer_used))

    def after_harvest(self):
        self.calls.append(("after_harvest", None))


class FakeModel:
    def __init__(self):
        self.calls = []
        self.balance = 0

        self.fields = [Field(True, "empty"), Field(True, "empty"), Field(True, "empty")]
        self.field_prices = [10, 20, 30]
        self.fertilizers = [
            Fertilizer("Супер добриво (-50%)", 3),
            Fertilizer("X", 5)
        ]

        self.buy_ok = True
        self.plant_ok = True
        self.harvest_ok = True
        self.sell_gained = 12
        self.grow_ms = 800

    def buy_fertilizer(self, fert_name):
        self.calls.append(("buy_fertilizer", fert_name))
        return self.buy_ok

    def plant_on_field(self, field_index, plant_name, fert_name):
        self.calls.append(("plant_on_field", (field_index, plant_name, fert_name)))
        if self.plant_ok:
            self.fields[field_index].state = "growing"
        return self.plant_ok

    def harvest(self, field_index):
        self.calls.append(("harvest", field_index))
        if self.harvest_ok:
            self.fields[field_index].state = "empty"
        return self.harvest_ok

    def get_grow_time(self, field_index):
        self.calls.append(("get_grow_time", field_index))
        return self.grow_ms

    def finish_growth(self, field_index):
        self.calls.append(("finish_growth", field_index))
        if self.fields[field_index].state == "growing":
            self.fields[field_index].state = "ready"

    def sell(self, plant_name):
        self.calls.append(("sell", plant_name))
        return self.sell_gained

    def save_state(self):
        self.calls.append(("save_state", None))




class TestFarmController(unittest.TestCase):
    def setUp(self):
        self._orig_view = FCmod.FarmView
        self._orig_missions = FCmod.MissionController
        self._orig_bonusdto = FCmod.FieldBonusDTO
        self._orig_sleep = time.sleep
        self._orig_thread = threading.Thread

        class ViewStub:
            calls = []
            root = DummyRoot()
            plant_var = DummyVar("Пшениця")
            fert_var = DummyVar("Без добрива")
            purchase_choice = None

            @classmethod
            def reset(cls):
                cls.calls = []
                cls.root = DummyRoot()
                cls.plant_var.set("Пшениця")
                cls.fert_var.set("Без добрива")
                cls.purchase_choice = None

            @classmethod
            def show_warning(cls, msg):
                cls.calls.append(("show_warning", msg))

            @classmethod
            def update_all(cls):
                cls.calls.append(("update_all", None))

            @classmethod
            def update_field_bg(cls, field_index, stage):
                cls.calls.append(("update_field_bg", (field_index, stage)))

            @classmethod
            def update_sell_info(cls, text):
                cls.calls.append(("update_sell_info", text))

            @classmethod
            def ask_field_purchase_mode(cls, field_number, base_price, bonus_price):
                cls.calls.append(("ask_field_purchase_mode", (field_number, base_price, bonus_price)))
                return cls.purchase_choice

        self.ViewStub = ViewStub
        self.ViewStub.reset()
        FCmod.FarmView = self.ViewStub

        FCmod.MissionController = SpyMissionsController

        class BonusDTO:
            def __init__(self, fertilizer_name, uses_left):
                self.fertilizer_name = fertilizer_name
                self.uses_left = uses_left

        FCmod.FieldBonusDTO = BonusDTO

        time.sleep = lambda _: None

        class ImmediateThread:
            def __init__(self, target, daemon=False):
                self._target = target

            def start(self):
                self._target()

        threading.Thread = ImmediateThread

        self.model = FakeModel()
        self.controller = FCmod.FarmController(self.model)

    def tearDown(self):
        FCmod.FarmView = self._orig_view
        FCmod.MissionController = self._orig_missions
        FCmod.FieldBonusDTO = self._orig_bonusdto
        time.sleep = self._orig_sleep
        threading.Thread = self._orig_thread



    def test_buy_fertilizer_success(self):
        self.model.buy_ok = True
        self.controller.buy_fertilizer("X")

        self.assertIn(("buy_fertilizer", "X"), self.model.calls)
        self.assertNotIn(("show_warning", "Недостатньо грошей або помилка покупки."), self.ViewStub.calls)
        self.assertIn(("update_all", None), self.ViewStub.calls)

    def test_buy_fertilizer_fail(self):
        self.model.buy_ok = False
        self.controller.buy_fertilizer("X")

        self.assertIn(("buy_fertilizer", "X"), self.model.calls)
        self.assertIn(("show_warning", "Недостатньо грошей або помилка покупки."), self.ViewStub.calls)
        self.assertIn(("update_all", None), self.ViewStub.calls)



    def test_field_clicked_locked_cancel(self):
        self.model.fields[0].unlocked = False
        self.ViewStub.purchase_choice = None

        self.controller.field_clicked(0)

        self.assertIn(("ask_field_purchase_mode", (1, 10, 22)), self.ViewStub.calls)
        self.assertNotIn(("save_state", None), self.model.calls)

    def test_field_clicked_locked_normal_not_enough(self):
        self.model.fields[0].unlocked = False
        self.ViewStub.purchase_choice = "normal"
        self.model.balance = 0

        self.controller.field_clicked(0)

        self.assertFalse(self.model.fields[0].unlocked)
        self.assertIn(("show_warning", "Недостатньо грошей, щоб відкрити поле 1. Потрібно 10₴."), self.ViewStub.calls)

    def test_field_clicked_locked_normal_success(self):
        self.model.fields[0].unlocked = False
        self.ViewStub.purchase_choice = "normal"
        self.model.balance = 10

        self.controller.field_clicked(0)

        self.assertTrue(self.model.fields[0].unlocked)
        self.assertIsNone(self.model.fields[0].bonus)
        self.assertEqual(self.model.balance, 0)
        self.assertIn(("save_state", None), self.model.calls)

        mc = self.controller.missions_controller
        self.assertIn(("after_field_unlocked", None), mc.calls)
        self.assertIn(("after_balance_change", None), mc.calls)

    def test_field_clicked_locked_bonus_not_enough(self):
        self.model.fields[0].unlocked = False
        self.ViewStub.purchase_choice = "bonus"
        self.model.balance = 0

        self.controller.field_clicked(0)

        self.assertFalse(self.model.fields[0].unlocked)
        self.assertIn(("show_warning","Недостатньо грошей, щоб купити поле 1 з бонусом. Потрібно 22₴."), self.ViewStub.calls)

    def test_field_clicked_locked_bonus_success(self):
        self.model.fields[0].unlocked = False
        self.ViewStub.purchase_choice = "bonus"
        self.model.balance = 22

        self.controller.field_clicked(0)

        self.assertTrue(self.model.fields[0].unlocked)
        self.assertIsNotNone(self.model.fields[0].bonus)
        self.assertEqual(self.model.fields[0].bonus.fertilizer_name, "Супер добриво (-50%)")
        self.assertEqual(self.model.fields[0].bonus.uses_left, 5)
        self.assertEqual(self.model.balance, 0)
        self.assertIn(("save_state", None), self.model.calls)


    def test_field_clicked_empty_plant_success_no_fert(self):
        self.model.fields[0].state = "empty"
        self.ViewStub.plant_var.set("Пшениця")
        self.ViewStub.fert_var.set("Без добрива")
        self.model.plant_ok = True

        self.controller.field_clicked(0)

        self.assertIn(("plant_on_field", (0, "Пшениця", None)), self.model.calls)
        self.assertIn(("update_field_bg", (0, 0)), self.ViewStub.calls)
        self.assertIn(("update_all", None), self.ViewStub.calls)

        mc = self.controller.missions_controller
        self.assertIn(("after_plant", False), mc.calls)

    def test_field_clicked_empty_plant_fail(self):
        self.model.fields[0].state = "empty"
        self.ViewStub.plant_var.set("Пшениця")
        self.ViewStub.fert_var.set("Без добрива")
        self.model.plant_ok = False

        self.controller.field_clicked(0)

        self.assertIn(("plant_on_field", (0, "Пшениця", None)), self.model.calls)
        self.assertIn(("show_warning", "Поле зайняте або немає добрива."), self.ViewStub.calls)

    def test_field_clicked_growing_shows_warning(self):
        self.model.fields[0].state = "growing"

        self.controller.field_clicked(0)

        self.assertIn(("show_warning", "Культура ще росте!"), self.ViewStub.calls)

    def test_field_clicked_ready_harvest_ok(self):
        self.model.fields[0].state = "ready"
        self.model.harvest_ok = True

        self.controller.field_clicked(0)

        self.assertIn(("harvest", 0), self.model.calls)
        self.assertIn(("update_field_bg", (0, 0)), self.ViewStub.calls)
        self.assertIn(("update_all", None), self.ViewStub.calls)

        mc = self.controller.missions_controller
        self.assertIn(("after_harvest", None), mc.calls)

    def test_field_clicked_ready_harvest_fail(self):
        self.model.fields[0].state = "ready"
        self.model.harvest_ok = False

        self.controller.field_clicked(0)

        self.assertIn(("harvest", 0), self.model.calls)
        self.assertIn(("show_warning", "Помилка збору!"), self.ViewStub.calls)
        self.assertIn(("update_all", None), self.ViewStub.calls)



    def test_start_growth_timer_grow_ms_le_0(self):
        self.model.grow_ms = 0
        self.controller.start_growth_timer(0)

        self.assertIn(("get_grow_time", 0), self.model.calls)
        self.assertNotIn(("finish_growth", 0), self.model.calls)

    def test_start_growth_timer_runs_worker_8_stages_and_finishes(self):
        self.model.fields[0].state = "growing"
        self.model.grow_ms = 800

        self.controller.start_growth_timer(0)

        stages = []
        for c in self.ViewStub.calls:
            if c[0] == "update_field_bg" and c[1][0] == 0:
                stages.append(c[1][1])

        self.assertEqual(stages, [1, 2, 3, 4, 5, 6, 7, 8])
        self.assertIn(("finish_growth", 0), self.model.calls)
        self.assertIn(("update_all", None), self.ViewStub.calls)



    def test_finish_growth_calls_model_and_updates(self):
        self.controller.finish_growth(0)
        self.assertIn(("finish_growth", 0), self.model.calls)
        self.assertIn(("update_all", None), self.ViewStub.calls)



    def test_sell_crop_gained_zero_shows_warning(self):
        self.model.sell_gained = 0
        self.controller.sell_crop("Пшениця")

        self.assertIn(("sell", "Пшениця"), self.model.calls)

        mc = self.controller.missions_controller
        self.assertIn(("after_balance_change", None), mc.calls)
        self.assertIn(("after_harvest", None), mc.calls)

        self.assertIn(("show_warning", "У амбарі немає такого урожаю."), self.ViewStub.calls)
        self.assertIn(("update_all", None), self.ViewStub.calls)

    def test_sell_crop_gained_positive_updates_info(self):
        self.model.sell_gained = 12
        self.controller.sell_crop("Пшениця")

        self.assertIn(("sell", "Пшениця"), self.model.calls)
        self.assertIn(("update_sell_info", "+12₴ отримано!"), self.ViewStub.calls)
        self.assertIn(("update_all", None), self.ViewStub.calls)


