import json
import os

class Plant:
    def __init__(self, name, grow_time, price, image_folder):
        self.name = name
        self.grow_time = grow_time
        self.price = price
        self.image_folder = image_folder

class WheatPlant(Plant):
    def __init__(self):
        super().__init__("Пшениця", 5000, 12, "IMG_wheat")

class CarrotPlant(Plant):
    def __init__(self):
        super().__init__("Морква", 3000, 8, "IMG_carrot")

class CornPlant(Plant):
    def __init__(self):
        super().__init__("Кукурудза", 8000, 20, "IMG_corn")

class WatermelonPlant(Plant):
    def __init__(self):
        super().__init__("Арбуз", 2000, 5, "IMG_watermelon")

class PineapplePlant(Plant):
    def __init__(self):
        super().__init__("Ананас", 4000, 9, "IMG_pineapple")

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
    SAVE_FILE= "../farm_save.txt"
    def __init__(self):
        self.balance = 50

        self.plants=[WheatPlant(), CarrotPlant(), CornPlant(), WatermelonPlant(), PineapplePlant()]
        self.fertilizers=[Fertilizer("Звичайне добриво (-20%)", 10, 0.8), Fertilizer("Супер добриво (-50%)", 20, 0.5)]
        self.fields=[Field(), Field(), Field(), Field()]
        self.ambar={"Пшениця": 0, "Морква": 0, "Кукурудза": 0, "Арбуз": 0, "Ананас": 0}
        self.warehouse={"Звичайне добриво (-20%)": 0, "Супер добриво (-50%)": 0}

    def buy_fertilizer(self, name):
        fert=next((f for f in self.fertilizers if f.name==name), None)
        if fert and self.balance >= fert.price:
            self.balance -= fert.price
            self.warehouse[fert.name] += 1
            self.save_state()
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
        self.save_state()
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
        self.save_state()
        return True

    def sell(self, plant_name):
        if self.ambar[plant_name] > 0:
            plant=next(p for p in self.plants if p.name == plant_name)
            self.ambar[plant_name] -= 1
            self.balance += plant.price
            self.save_state()
            return plant.price
        return 0

    def save_state(self):
        data={"balance": self.balance, "ambar": self.ambar, "warehouse": self.warehouse}
        try:
            with open(self.SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def load_state(self):
        try:
            with open(self.SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            return

        self.balance = data.get("balance", self.balance)

        saved_ambar = data.get("ambar", {})
        for name in self.ambar.keys():
            self.ambar[name] = int(saved_ambar.get(name, 0))

        saved_warehouse = data.get("warehouse", {})
        for name in self.warehouse.keys():
            self.warehouse[name] = int(saved_warehouse.get(name, 0))