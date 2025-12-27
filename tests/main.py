import unittest

from tests.test_FarmModel import TestFarmModel
from tests.test_FarmController import TestFarmController
from tests.test_MissionsController import TestMissionsController

FarmModel=TestFarmModel()
FarmController=TestFarmController()
MissionsController=TestMissionsController()

if __name__ == "__main__":
    unittest.main()