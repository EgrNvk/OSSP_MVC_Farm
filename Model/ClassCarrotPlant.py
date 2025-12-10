from Model.ClassPlant import Plant, IMAGE_PATHS

class CarrotPlant(Plant):
    def __init__(self):
        super().__init__("Морква", 3000, 8, IMAGE_PATHS.get("Морква"))