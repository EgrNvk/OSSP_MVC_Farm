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
        field = self.fields[field_index]

        if field.state != "empty":
            return False

        plant = None
        for p in self.plants:
            if p.name == plant_name:
                plant = p
                break

        fertilizer = None
        if fert_name is not None:
            if self.warehouse[fert_name] <= 0:
                return False

            for f in self.fertilizers:
                if f.name == fert_name:
                    fertilizer = f
                    break

            self.warehouse[fert_name] -= 1

        field.state = "growing"
        field.plant = plant
        field.fertilizer = fertilizer
        return True


def get_grow_time(self, field_index):
    field = self.fields[field_index]
    if field.plant is None:
        return 0

    base = field.plant.grow_time
    if field.fertilizer is None:
        return base

    return int(base * field.fertilizer.multiplier)

def finish_growth(self, field_index):
    field = self.fields[field_index]
    if field.state == "growing":
        field.state = "ready"

def harvest(self, field_index):
    field = self.fields[field_index]

    if field.state != "ready":
        return False

    name = field.plant.name
    self.ambar[name] += 1

    field.state = "empty"
    field.plant = None
    field.fertilizer = None
    return True

def sell(self, plant_name):
    if self.ambar[plant_name] <= 0:
        return 0

    plant = None
    for p in self.plants:
        if p.name == plant_name:
            plant = p
            break

    self.ambar[plant_name] -= 1
    self.balance += plant.price