from app.Model.Plant import Plant

class CarrotPlant(Plant):
    def __init__(self):
        super().__init__("Морква", 3000, 8)