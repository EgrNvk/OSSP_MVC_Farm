from Model.ClassPlant import Plant, IMAGE_PATHS

class WheatPlant(Plant):
    def __init__(self):
        super().__init__("Пшениця", 5000, 12, IMAGE_PATHS.get("Пшениця"))