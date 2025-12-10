from Model.ClassPlant import Plant, IMAGE_PATHS

class CornPlant(Plant):
    def __init__(self):
        super().__init__("Кукурудза", 8000, 20, IMAGE_PATHS.get("Кукурудза"))