from pathlib import Path
import json

class ResourceService:
    def __init__(self):
        self.PROJECT_ROOT = Path(__file__).resolve().parents[1]

        self.RESOURCES_DIR = self.PROJECT_ROOT / "Resources"

        self.RESOURCES_FILE = self.RESOURCES_DIR / "resources.json"

        with open(self.RESOURCES_FILE, "r", encoding="utf-8") as f:
            self.RESOURCES = json.load(f)

        self.IMAGE_FOLDERS = {
            name: self.RESOURCES_DIR / rel_path
            for name, rel_path in self.RESOURCES.get("image_folders", {}).items()
        }

    def get_image_path(self, crop: str, stage: int) -> Path:
        return self.IMAGE_FOLDERS[crop] / f"{stage}.png"