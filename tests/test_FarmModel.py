import unittest
from app.Model.FarmModel import FarmModel

class TestFarmModel(unittest.TestCase):
    def test_initial_balance_exists(self):
        model = FarmModel()
        self.assertIsNotNone(model.balance)
