# import json
# from pathlib import Path
#
# RESOURCES_FILE = Path(__file__).parent.parent/("resources.json")
#
# with open(RESOURCES_FILE, "r", encoding="utf-8") as f:
#     RES=json.load(f)
#
# IMAGE_PATHS=RES.get("images", {})

class Plant:
    def __init__(self, name, grow_time, price):
        self.name = name
        self.grow_time = grow_time
        self.price = price
        self.stage = 0