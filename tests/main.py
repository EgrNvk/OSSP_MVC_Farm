import unittest

from tests.test_FarmModel import TestFarmModel
from tests.test_FarmController import TestFarmController
from tests.test_MissionsController import TestMissionsController
from tests.test_Resource_Service import TestResourceService

FarmModel=TestFarmModel()
FarmController=TestFarmController()
MissionsController=TestMissionsController()
ResourceService=TestResourceService()

if __name__ == "__main__":
    unittest.main()