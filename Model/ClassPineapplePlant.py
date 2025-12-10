from Model.ClassPlant import Plant, IMAGE_PATHS

class PineapplePlant(Plant):
    def __init__(self):
        super().__init__("Ананас", 4000, 9, IMAGE_PATHS.get("Ананас"))