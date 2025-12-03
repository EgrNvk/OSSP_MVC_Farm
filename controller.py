import threading
import time
import view


class FarmController:
    def __init__(self, model):
        self.model = model

    def buy_fertilizer(self, fert_name):
        ok = self.model.buy_fertilizer(fert_name)
        if not ok:
            view.show_warning("Недостатньо грошей для покупки добрива.")
        view.update_all()

    def field_clicked(self, field_index):
        field = self.model.fields[field_index]

        if field.state == "empty":
            plant_name = view.plant_var.get()
            fert_name = view.fert_var.get()
            if fert_name == "Без добрива":
                fert_name = None

            ok = self.model.plant_on_field(field_index, plant_name, fert_name)
            if not ok:
                view.show_warning("Не вдалося посадити. Немає добрива або поле не пусте.")
                view.update_all()
                return

            view.update_all()
            self.start_growth_timer(field_index)

        elif field.state == "growing":
            view.show_warning("Культура ще росте!")

        elif field.state == "ready":
            ok = self.model.harvest(field_index)
            if not ok:
                view.show_warning("Не вдалося зібрати урожай.")
            view.update_all()

    def start_growth_timer(self, field_index):
        grow_ms = self.model.get_grow_time(field_index)

        def worker():
            time.sleep(grow_ms / 1000.0)
            view.root.after(0, lambda: self.finish_growth(field_index))

        threading.Thread(target=worker, daemon=True).start()

    def finish_growth(self, field_index):
        self.model.finish_growth(field_index)
        view.update_all()

    def sell_crop(self, plant_name):
        gained = self.model.sell(plant_name)

        if gained == 0:
            view.show_warning("У амбарі немає такого урожаю.")
        else:
            view.update_sell_info(f"Продано 1 шт. {plant_name} за {gained}₴")

        view.update_all()