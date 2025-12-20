import threading
import time

from DTO.DTO import FieldBonusDTO
from View import view
from Services.Logger_Service import logger
from Controller.MissionsController import MissionController

class FarmController:
    def __init__(self, model):
        self.model = model
        self.missions_controller = MissionController(model)
        logger.info("FarmController створено")
        self.missions_controller.sync_all()

    def buy_fertilizer(self, fert_name):
        logger.debug(f"Спроба купити добрево: {fert_name}")
        ok = self.model.buy_fertilizer(fert_name)
        if not ok:
            logger.warning(f"Не вдалося купити добрево: {fert_name}")
            view.show_warning("Недостатньо грошей або помилка покупки.")
        else:
            logger.info(f"Добрево куплено: {fert_name}")
        view.update_all()

    def field_clicked(self, field_index):
        logger.debug(f"Клік по полю {field_index+1}")
        field = self.model.fields[field_index]

        if not field.unlocked:
            logger.info(f"Поле {field_index+1} спроба покупкі заблакованого полю")
            base_price = self.model.field_prices[field_index]

            super_fert = next(
                (f for f in self.model.fertilizers if f.name == "Супер добриво (-50%)"),
                None
            )
            super_price = super_fert.price if super_fert else 0

            bonus_price = base_price + super_price * 4

            choice = view.ask_field_purchase_mode(
                field_index + 1,
                base_price,
                bonus_price
            )

            if choice is None:
                logger.info(f"Покупку поля {field_index+1} скасовано")
                return

            if choice == "bonus":
                logger.warning(f"Недостатньо коштів для покупки з бонусом поля {field_index+1}")
                if self.model.balance < bonus_price:
                    view.show_warning(
                        f"Недостатньо грошей, щоб купити поле {field_index + 1} з бонусом. "
                        f"Потрібно {bonus_price}₴."
                    )
                    return

                logger.info(f"Поле {field_index+1} куплено з бонусом")
                self.model.balance -= bonus_price
                field.unlocked = True
                self.missions_controller.after_field_unlocked()
                self.missions_controller.after_balance_change()
                if super_fert:
                    field.bonus = FieldBonusDTO(
                        fertilizer_name=super_fert.name,
                        uses_left=5
                    )
                self.model.save_state()
                view.update_all()
                return

            if choice == "normal":
                if self.model.balance < base_price:
                    logger.warning(f"Недостатньо коштів для покупки з бонусом поля {field_index+1}")
                    view.show_warning(
                        f"Недостатньо грошей, щоб відкрити поле {field_index + 1}. "
                        f"Потрібно {base_price}₴."
                    )
                    return

                logger.info(f"Поле {field_index+1} куплено без бонуса")
                self.model.balance -= base_price
                field.unlocked = True
                field.bonus = None
                self.missions_controller.after_field_unlocked()
                self.missions_controller.after_balance_change()
                self.model.save_state()
                view.update_all()
                return

        if field.state == "empty":
            plant_name = view.plant_var.get()
            fert_name = view.fert_var.get()
            if fert_name == "Без добрива":
                fert_name = None
            logger.info(f"Посадка на полі {field_index+1}: рослина {plant_name}, добрево {fert_name}")

            ok = self.model.plant_on_field(field_index, plant_name, fert_name)
            if not ok:
                logger.warning(f"Не вдалося посадити рослину {plant_name} на полі {field_index+1}")
                view.show_warning("Поле зайняте або немає добрива.")
                return

            self.missions_controller.after_plant(fertilizer_used=(fert_name is not None))

            view.update_field_bg(field_index, 0)
            view.update_all()
            self.start_growth_timer(field_index)

        elif field.state == "growing":
            view.show_warning("Культура ще росте!")

        elif field.state == "ready":
            logger.info(f"Збір уражаю з поля {field_index+1}")
            ok = self.model.harvest(field_index)
            self.missions_controller.after_harvest()
            if ok:
                view.update_field_bg(field_index, 0)
            else:
                logger.error(f"Помилка збору уражая з поля {field_index+1}")
                view.show_warning("Помилка збору!")
            view.update_all()

    def start_growth_timer(self, field_index):
        grow_ms = self.model.get_grow_time(field_index)
        if grow_ms <= 0:
            return

        step_time = (grow_ms / 1000) / 8

        def worker():
            for stage in range(1, 9):
                time.sleep(step_time)

                def ui_update(s=stage):
                    field = self.model.fields[field_index]
                    if field.state == "growing":
                        view.update_field_bg(field_index, s)

                view.root.after(0, ui_update)

            view.root.after(0, lambda: self.finish_growth(field_index))

        threading.Thread(target=worker, daemon=True).start()

    def finish_growth(self, field_index):
        self.model.finish_growth(field_index)
        view.update_all()

    def sell_crop(self, plant_name):
        logger.debug(f"Спроба продажу: {plant_name}")
        gained = self.model.sell(plant_name)
        self.missions_controller.after_balance_change()

        if gained == 0:
            logger.warning(f"Продаж не вдався: {plant_name}")
            view.show_warning("У амбарі немає такого урожаю.")
        else:
            logger.info(f"Продано {plant_name}, отримано {gained}₴")
            view.update_sell_info(f"+{gained}₴ отримано!")

        view.update_all()