class Plant:
    def __init__(self, name, grow_time, price, image_folder):
        self.name = name
        self.grow_time = grow_time
        self.price = price
        self.image_folder = image_folder

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

        self.plants=[
            Plant("Пшениця", 5000, 12, "IMG_wheat"),
            Plant("Морква", 3000, 8, "IMG_carrot"),
            Plant("Кукурудза", 8000, 20, "img_corn")
        ]
        self.fertilizers=[Fertilizer("Звичайне добриво (-20%)", 10, 0.8), Fertilizer("Супер добриво (-50%)", 20, 0.5)]
        self.fields=[Field(), Field(), Field(), Field()]
        self.ambar={"Пшениця": 0, "Морква": 0, "Кукурудза": 0}
        self.warehouse={"Звичайне добриво (-20%)": 0, "Супер добриво (-50%)": 0}

    def buy_fertilizer(self, name):
        fert=next((f for f in self.fertilizers if f.name==name), None)
        if fert and self.balance >= fert.price:
            self.balance -= fert.price
            self.warehouse[fert.name] += 1
            return True
        return False

    def plant_on_field(self, index, plant_name, fert_name=None):
        field = self.fields[index]
        if field.state != "empty":
            return False

        plant=next((p for p in self.plants if p.name==plant_name), None)
        fert=next((f for f in self.fertilizers if f.name==fert_name), None) if fert_name else None

        if fert:
            if self.warehouse[fert.name] <= 0:
                return False
            self.warehouse[fert.name] -= 1

        field.plant=plant
        field.fertilizer=fert
        field.state="growing"
        return True

    def get_grow_time(self, index):
        field = self.fields[index]
        if not field.plant:
            return 0

        base = field.plant.grow_time
        if field.fertilizer:
            return int(base * field.fertilizer.multiplier)
        return base

    def finish_growth(self, index):
        field = self.fields[index]
        if field.state == "growing":
            field.state = "ready"

    def harvest(self, index):
        field = self.fields[index]

        if field.state != "ready":
            return False

        self.ambar[field.plant.name] += 1
        field.state = "empty"
        field.plant = None
        field.fertilizer = None
        return True

    def sell(self, plant_name):
        if self.ambar[plant_name] > 0:
            plant=next(p for p in self.plants if p.name == plant_name)
            self.ambar[plant_name] -= 1
            self.balance += plant.price
            return plant.price
        return 0