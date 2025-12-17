from Model.ClassFarmModel import FarmModel
from View import view
from Controller.controller import FarmController
from Services.Logger_Service import logger

def main():
    logger.info("")
    logger.info("Запуск OSSP_MVC_Farm")
    try:
        logger.debug("Ініціалізація моделі")
        model = FarmModel()
        logger.debug("Завантаження стану")
        model.load_state()
        logger.debug("Ініціалізація контролеру")
        controller = FarmController(model)
        logger.debug("Створення GUI")
        root = view.create_view(model, controller)
        logger.info("Запуск mainloop()")
        root.mainloop()
        logger.info("Програма завершила роботу без помилок")
    except Exception:
        logger.critical("Критична помилка в main()", exc_info=True)

if __name__ == "__main__":
    main()