class Plant:
    def __init__(self, name, grow_time, price):
        self.name = name
        self.grow_time = grow_time
        self.price = price

class Fertilizer:
    def __init__(self, name, price, multiplier):
        self.name = name
        self.price = price
        self.multiplier = multiplier

class Field:
    def __init__(self):
        self.state="empty"
        self.plant=None
        self.fertilizer=None

class FarmModel:
    def __init__(self):
        self.balance = 50

        self.plants=[Plant("Пшениця", 5000, 12), Plant("Морква", 3000, 8), Plant("Кукурудза", 8000, 20)]
        self.fertilizers=[Fertilizer("Звичайне добриво (-20%)", 10, 0.8), Fertilizer("Супер добриво (-50%)", 20, 0.5)]
        self.fields=[Field(), Field(), Field(), Field()]
        self.ambar={"Пшениця": 0, "Морква": 0, "Кукурудза": 0}
        self.warehouse={"Звичайне добриво (-20%)": 0, "Супер добриво (-50%)": 0}

    def buy_fertilizer(self, fert_name):
        fertilizer=None
        for f in self.fertilizers:
            if f.name==fert_name:
                fertilizer=f
                break

        if self.balance<fertilizer.price:
            return False

        self.balance-=fertilizer.price
        self.warehouse[fertilizer.name]+=1
        return True

    def plant_on_field(self, field_index, plant_name, fert_name=None):
        pass

    def get_grow_time(self, field_index):
        pass

    def finish_growth(self, field_index):
        pass

    def harvest(self, field_index):
        pass

    def sell(self, plant_name):
        pass

    def plant_on_field(self, field_index, plant_name, fert_name=None):
        pass

