class FieldBonusDTO:
    def __init__(self, fertilizer_name: str, uses_left: int=5):
        self.fertilizer_name = fertilizer_name
        self.uses_left = uses_left