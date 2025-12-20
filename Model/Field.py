from DTO.FieldBonusDTO import FieldBonusDTO

class Field:
    def __init__(self):
        self.state="empty"
        self.plant=None
        self.fertilizer=None

        self.unlocked=False
        self.bonus: FieldBonusDTO | None = None