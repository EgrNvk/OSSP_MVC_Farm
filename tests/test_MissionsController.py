import unittest

from app.Controller.MissionsController import MissionController



class Field:
    def __init__(self, unlocked=False):
        self.unlocked = unlocked


class MissionsState:
    def __init__(self):
        self.money = 0
        self.unlocked_fields = 0
        self.total_fields = 0
        self.wheat_count = 0

        self.current_session_time = 0
        self.longest_session_time = 0
        self.longest_session_done = False

        self.total_harvest = 0
        self.organic_plantings = 0

        self.check_all_calls = 0

    def check_all(self):
        self.check_all_calls += 1


class FakeModel:
    def __init__(self):
        self.balance = 0
        self.fields = []
        self.ambar = {"Пшениця": 0}
        self.missions = MissionsState()



class TestMissionsController(unittest.TestCase):
    def setUp(self):
        self.model = FakeModel()
        self.controller = MissionController(self.model)

    def test_sync_all_updates_basic_counters_and_calls_check_all(self):
        self.model.balance = 123
        self.model.fields = [Field(True), Field(False), Field(True)]
        self.model.ambar = {"Пшениця": 7, "Морква": 2}

        m = self.model.missions
        m.current_session_time = 5
        m.longest_session_time = 10
        m.longest_session_done = False

        self.controller.sync_all()

        self.assertEqual(m.money, 123)
        self.assertEqual(m.unlocked_fields, 2)
        self.assertEqual(m.total_fields, 3)
        self.assertEqual(m.wheat_count, 7)
        self.assertEqual(m.total_harvest, 9)
        self.assertEqual(m.check_all_calls, 1)

        self.assertEqual(m.longest_session_time, 10)
        self.assertFalse(m.longest_session_done)

    def test_sync_all_updates_longest_session_when_current_is_greater(self):
        self.model.balance = 1
        self.model.fields = [Field(True)]
        self.model.ambar = {"Пшениця": 0}

        m = self.model.missions
        m.current_session_time = 12
        m.longest_session_time = 10
        m.longest_session_done = False

        self.controller.sync_all()

        self.assertEqual(m.longest_session_time, 12)
        self.assertTrue(m.longest_session_done)
        self.assertEqual(m.check_all_calls, 1)

    def test_after_field_unlocked_recounts_unlocked_and_calls_check_all(self):
        self.model.fields = [Field(True), Field(False), Field(True), Field(True)]
        m = self.model.missions
        m.unlocked_fields = 0

        self.controller.after_field_unlocked()

        self.assertEqual(m.unlocked_fields, 3)
        self.assertEqual(m.check_all_calls, 1)

    def test_after_plant_without_fertilizer_increments_organic_and_calls_check_all(self):
        m = self.model.missions
        m.organic_plantings = 0

        self.controller.after_plant(fertilizer_used=False)

        self.assertEqual(m.organic_plantings, 1)
        self.assertEqual(m.check_all_calls, 1)

    def test_after_plant_with_fertilizer_does_nothing(self):
        m = self.model.missions
        m.organic_plantings = 5

        self.controller.after_plant(fertilizer_used=True)

        self.assertEqual(m.organic_plantings, 5)
        self.assertEqual(m.check_all_calls, 0)

    def test_after_harvest_updates_wheat_count_and_calls_check_all(self):
        self.model.ambar = {"Пшениця": 11, "Морква": 4}
        m = self.model.missions
        m.wheat_count = 0

        self.controller.after_harvest()

        self.assertEqual(m.wheat_count, 11)
        self.assertEqual(m.check_all_calls, 1)

    def test_after_balance_change_updates_money_and_calls_check_all(self):
        self.model.balance = 777
        m = self.model.missions
        m.money = 0

        self.controller.after_balance_change()

        self.assertEqual(m.money, 777)
        self.assertEqual(m.check_all_calls, 1)

    def test_after_tick_increments_time_and_calls_sync_all(self):
        self.model.balance = 50
        self.model.fields = [Field(True), Field(False)]
        self.model.ambar = {"Пшениця": 3, "Морква": 1}

        m = self.model.missions
        m.current_session_time = 9
        m.longest_session_time = 0
        m.check_all_calls = 0

        self.controller.after_tick()

        self.assertEqual(m.current_session_time, 10)
        self.assertEqual(m.money, 50)
        self.assertEqual(m.unlocked_fields, 1)
        self.assertEqual(m.total_fields, 2)
        self.assertEqual(m.wheat_count, 3)
        self.assertEqual(m.total_harvest, 4)
        self.assertEqual(m.check_all_calls, 1)


