import json
from pathlib import Path

from Model.ClassCarrotPlant import CarrotPlant
from Model.ClassCornPlant import CornPlant
from Model.ClassFertilizer import Fertilizer
from Model.ClassField import Field
from Model.ClassPineapplePlant import PineapplePlant
from Model.ClassWatermelonPlant import WatermelonPlant
from Model.ClassWheatPlant import WheatPlant

# RESOURCES_FILE = Path(__file__).parent.parent/("resources.json")
#
# with open(RESOURCES_FILE, "r", encoding="utf-8") as f:
#     RES=json.load(f)
#
# SAVE_FILE=RES.get("save_file", "farm_save.txt")
from Services.Resource_Service import ResourceService



class FarmModel:
    # SAVE_FILE= "../farm_save.txt"
    def __init__(self):
        self.balance = 50
        service = ResourceService()
        self.save_file = service.RESOURCES.get("save_file", "farm_save.txt")
        self.plants=[WheatPlant(), CarrotPlant(), CornPlant(), WatermelonPlant(), PineapplePlant()]
        self.fertilizers=[Fertilizer("Звичайне добриво (-20%)", 10, 0.8), Fertilizer("Супер добриво (-50%)", 20, 0.5)]
        self.max_fields=8
        self.field_prices=[0, 0, 0, 0, 150, 175, 200, 250]

        self.fields=[]
        for i in range(self.max_fields):
            field=Field()
            field.unlocked=(i<4)
            self.fields.append(field)

        self.ambar={"Пшениця": 0, "Морква": 0, "Кукурудза": 0, "Арбуз": 0, "Ананас": 0}
        self.warehouse={"Звичайне добриво (-20%)": 0, "Супер добриво (-50%)": 0}

        self.load_state()

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
        data={"balance": self.balance, "ambar": self.ambar, "warehouse": self.warehouse, "fields": [{"unlocked": getattr(f, "unlocked", False)} for f in self.fields]}
        try:
            with open(self.save_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def load_state(self):
        try:
            with open(self.save_file, "r", encoding="utf-8") as f:
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

        saved_fields = data.get("fields")
        if saved_fields:
            for i, fd in enumerate(saved_fields):
                if i >= len(self.fields):
                    break
                field = self.fields[i]

                default_unlocked=(i<4)
                field.unlocked=fd.get("unlocked", default_unlocked)
        else:
            for i, field in enumerate(self.fields):
                field.unlocked=(i<4)