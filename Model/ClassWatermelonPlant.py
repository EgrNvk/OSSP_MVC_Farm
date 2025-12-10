from Model.ClassPlant import Plant, IMAGE_PATHS

class WatermelonPlant(Plant):
    def __init__(self):
        super().__init__("Арбуз", 2000, 5, IMAGE_PATHS.get("Арбуз"))