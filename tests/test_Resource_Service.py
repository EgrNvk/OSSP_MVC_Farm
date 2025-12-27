import unittest
from pathlib import Path

from app.Services.Resource_Service import ResourceService


class TestResourceService(unittest.TestCase):

    def test_get_image_path_returns_correct_path(self):
        service = ResourceService()

        crop = "Пшениця"
        stage = 3

        base_folder = service.IMAGE_FOLDERS[crop]
        path = service.get_image_path(crop, stage)

        self.assertIsInstance(path, Path)
        self.assertEqual(path, base_folder / "3.png")
        self.assertEqual(path.name, "3.png")