from Model.Plant import Plant

class WheatPlant(Plant):
    def __init__(self):
        super().__init__("Пшениця", 5000, 12)