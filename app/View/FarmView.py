import tkinter as tk
from tkinter import messagebox
from app.Services.Logger_Service import logger

from app.Services.Resource_Service import ResourceService
res = ResourceService()
current_images = [None, None, None, None, None, None, None, None]

# RESOURCES_FILE = Path(__file__).parent.parent/("resources.json")
#
# with open(RESOURCES_FILE, "r", encoding="utf-8") as f:
#     RES=json.load(f)
#
# IMAGE_FOLDERS=RES.get("image_folders", {})

root = None
model = None
controller = None

balance_label = None
ambar_label = None
warehouse_label = None

missions_frame = None
missions_labels = []

field_buttons = []
field_labels = []

plant_var = None
fert_var = None
sell_var = None
sell_info_label = None


def create_view(app_model, app_controller):
    logger.info("View Start")
    global root, model, controller
    global balance_label, ambar_label, warehouse_label
    global field_buttons, field_labels, plant_var, fert_var, sell_var, sell_info_label
    global current_images

    model = app_model
    controller = app_controller

    # root = tk.Tk()
    # root.title("Ферма")
    # root.geometry("1000x1150")
    root = tk.Tk()
    root.title("Ферма")
    root.geometry("1200x900")

    main_frame = tk.Frame(root)
    main_frame.pack(fill="both", expand=True)

    left_frame = tk.Frame(main_frame)
    left_frame.pack(side="left", fill="both", expand=True)

    right_frame = tk.Frame(main_frame, width=500)
    right_frame.pack(side="right", fill="y")
    right_frame.pack_propagate(False)

    PAD = 15

    balance_label = tk.Label(left_frame, font=("Arial", 16))
    balance_label.pack(fill="x",pady=5)

    ambar_label = tk.Label(left_frame, font=("Arial", 12))
    ambar_label.pack(fill="x",pady=3)

    global missions_frame, missions_labels

    missions_frame = tk.Frame(right_frame, bd=2, relief="groove", padx=10, pady=10)
    missions_frame.pack(fill="both", expand=True, padx=PAD, pady=10)

    tk.Label(missions_frame, text="Місії", font=("Arial", 12, "bold")).pack(anchor="w")

    missions_labels.clear()
    for _ in range(12):
        lbl = tk.Label(missions_frame, font=("Arial", 11), anchor="w", justify="left")
        lbl.pack(anchor="w")
        missions_labels.append(lbl)

    warehouse_label = tk.Label(left_frame, font=("Arial", 12))
    warehouse_label.pack(fill="x", pady=10)

    frame_select = tk.Frame(left_frame, bd=2, relief="groove", padx=10, pady=10)
    frame_select.pack(fill="x", padx=PAD, pady=10)
    select_center = tk.Frame(frame_select)
    select_center.pack(expand=True)

    tk.Label(select_center,text="Рослина:").grid(row=0, column=0, padx=5, pady=3)
    plant_var = tk.StringVar(value=model.plants[0].name)
    tk.OptionMenu(select_center,plant_var,*[p.name for p in model.plants]).grid(row=0, column=1, padx=5, pady=3)

    tk.Label(select_center,text="Добриво:").grid(row=1, column=0, padx=5, pady=3)
    fert_var = tk.StringVar(value="Без добрива")
    tk.OptionMenu(select_center,fert_var,"Без добрива",*[f.name for f in model.fertilizers]).grid(row=1, column=1, padx=5, pady=3)

    frame_fields = tk.Frame(left_frame, bd=2, relief="groove", padx=10, pady=10)
    frame_fields.pack(fill="x", padx=PAD, pady=10)

    for col in range(4):
        frame_fields.grid_columnconfigure(col, weight=1)

    for row in range(4):
        frame_fields.grid_rowconfigure(row, weight=1)

    field_buttons.clear()
    field_labels.clear()

    btn1 = tk.Button(frame_fields, compound="top", command=lambda: on_field_click(0))
    btn1.grid(row=0, column=0, padx=20, pady=5)
    field_buttons.append(btn1)
    lbl1 = tk.Label(frame_fields, text="Поле 1")
    lbl1.grid(row=1, column=0, padx=20, pady=5)
    field_labels.append(lbl1)

    btn2 = tk.Button(frame_fields, compound="top", command=lambda: on_field_click(1))
    btn2.grid(row=0, column=1, padx=20, pady=5)
    field_buttons.append(btn2)
    lbl2 = tk.Label(frame_fields, text="Поле 2")
    lbl2.grid(row=1, column=1, padx=20, pady=5)
    field_labels.append(lbl2)

    btn3 = tk.Button(frame_fields, compound="top", command=lambda: on_field_click(2))
    btn3.grid(row=0, column=2, padx=20, pady=5)
    field_buttons.append(btn3)
    lbl3 = tk.Label(frame_fields, text="Поле 3")
    lbl3.grid(row=1, column=2, padx=20, pady=5)
    field_labels.append(lbl3)

    btn4 = tk.Button(frame_fields, compound="top", command=lambda: on_field_click(3))
    btn4.grid(row=0, column=3, padx=20, pady=5)
    field_buttons.append(btn4)
    lbl4 = tk.Label(frame_fields, text="Поле 4")
    lbl4.grid(row=1, column=3, padx=20, pady=5)
    field_labels.append(lbl4)

    btn5 = tk.Button(frame_fields, compound="top", command=lambda: on_field_click(4))
    btn5.grid(row=2, column=0, padx=20, pady=5)
    field_buttons.append(btn5)
    lbl5 = tk.Label(frame_fields, text="Поле 5")
    lbl5.grid(row=3, column=0, padx=20, pady=5)
    field_labels.append(lbl5)

    btn6 = tk.Button(frame_fields, compound="top", command=lambda: on_field_click(5))
    btn6.grid(row=2, column=1, padx=20, pady=5)
    field_buttons.append(btn6)
    lbl6 = tk.Label(frame_fields, text="Поле 6")
    lbl6.grid(row=3, column=1, padx=20, pady=5)
    field_labels.append(lbl6)

    btn7 = tk.Button(frame_fields, compound="top", command=lambda: on_field_click(6))
    btn7.grid(row=2, column=2, padx=20, pady=5)
    field_buttons.append(btn7)
    lbl7 = tk.Label(frame_fields, text="Поле 7")
    lbl7.grid(row=3, column=2, padx=20, pady=5)
    field_labels.append(lbl7)

    btn8 = tk.Button(frame_fields, compound="top", command=lambda: on_field_click(7))
    btn8.grid(row=2, column=3, padx=20, pady=5)
    field_buttons.append(btn8)
    lbl8 = tk.Label(frame_fields, text="Поле 8")
    lbl8.grid(row=3, column=3, padx=20, pady=5)
    field_labels.append(lbl8)

    for i in range(8):
        update_field_bg(i, 0)

    shop_sell_frame = tk.Frame(left_frame)
    shop_sell_frame.pack(fill="x", padx=PAD, pady=10)

    frame_shop = tk.Frame(shop_sell_frame, bd=2, relief="groove", padx=10, pady=10)
    frame_shop.pack(side="left", fill="both", expand=True, padx=5)

    tk.Label(frame_shop, text="Магазин добрив").pack()
    shop_center = tk.Frame(frame_shop)
    shop_center.pack(expand=True)

    for fert in model.fertilizers:
        tk.Button(
            frame_shop,
            text=f"Купити {fert.name} ({fert.price}₴)",
            command=lambda name=fert.name: on_buy_fertilizer(name)
        ).pack(pady=2)

    frame_sell = tk.Frame(shop_sell_frame, bd=2, relief="groove", padx=10, pady=10)
    frame_sell.pack(side="left", fill="both", expand=True, padx=5)

    tk.Label(frame_sell, text="Продаж").grid(row=0, column=0, columnspan=2)

    sell_var = tk.StringVar(value=model.plants[0].name)
    tk.OptionMenu(frame_sell, sell_var, *[p.name for p in model.plants]).grid(row=1, column=0)
    frame_sell.grid_columnconfigure(0, weight=1)
    frame_sell.grid_columnconfigure(1, weight=1)
    tk.Button(
        frame_sell,
        text="Продати 1 шт",
        command=on_sell_click
    ).grid(row=1, column=1)

    sell_info_label = tk.Label(frame_sell, text="", fg="gray")
    sell_info_label.grid(row=2, column=0, columnspan=2)

    update_all()

    TICK_MS = 60000

    def start_session_timer():
        controller.missions_controller.after_tick()
        root.after(TICK_MS, start_session_timer)

    start_session_timer()

    return root


def update_field_bg(index, stage):
    field = model.fields[index]

    if not getattr(field, "unlocked", True):
        field_buttons[index].config(
            image="",
            text="Заблоковано",
            compound="center"
        )
        current_images[index] = None
        return

    plant = field.plant
    if plant is None:
        crop_key = "Пшениця"
        stage = 0
    else:
        crop_key = plant.name

    img_path = res.get_image_path(crop_key, stage)

    try:
        img = tk.PhotoImage(file=str(img_path))
    except Exception:
        logger.warning(f"View не вдалося завантажити зображення (field={index+1}, stage={stage}, path={img_path})")
        return

    current_images[index] = img
    field_buttons[index].config(image=img, text="", compound="top")
    field_buttons[index].image = img


def update_balance():
    balance_label.config(text=f"Баланс: {model.balance}₴")


def update_ambar():
    text = ", ".join([f"{k}: {v}" for k, v in model.ambar.items()])
    ambar_label.config(text="Амбар: " + text)


def update_warehouse():
    text = ", ".join([f"{k}: {v}" for k, v in model.warehouse.items()])
    warehouse_label.config(text="Склад добрив: " + text)


def update_all():
    update_balance()
    update_ambar()
    update_warehouse()
    update_missions()

    for i, field in enumerate(model.fields):
        if not getattr(field, "unlocked", True):
            txt = f"Поле {i + 1}: заблоковано"
        elif field.state == "empty":
            txt = f"Поле {i + 1}: пусто"
        elif field.state == "growing":
            txt = f"Поле {i + 1}: росте"
        else:
            txt = f"Поле {i + 1}: ГОТОВО"

        bonus=getattr(field, "bonus", None)
        if bonus and getattr(field, "unlocked", False) and bonus.uses_left>0:
            txt+=f" (бонус x{bonus.uses_left})"

        field_labels[i].config(text=txt)

        if field.state=="ready":
            update_field_bg(i, 8)
        else:
            update_field_bg(i, 0)


def on_buy_fertilizer(name):
    controller.buy_fertilizer(name)


def on_field_click(index):
    controller.field_clicked(index)


def on_sell_click():
    controller.sell_crop(sell_var.get())


def update_sell_info(text):
    sell_info_label.config(text=text)


def show_warning(msg):
    logger.warning(f"View: show_warning={msg}")
    messagebox.showwarning("Помилка", msg)


def ask_field_purchase_mode(field_number: int, base_price: int, bonus_price: int):
    msg = (
        f"Поле {field_number} заблоковано.\n\n"
        f"Варіанти покупки:\n"
        f"• Звичайне поле: {base_price}₴\n"
        f"• Поле з бонусом (5 посівів Супер добрива -50%): {bonus_price}₴\n\n"
        f"Натисніть 'Так', щоб купити з бонусом.\n"
        f"Натисніть 'Ні', щоб купити без бонусу.\n"
        f"Натисніть 'Cancel', щоб скасувати."
    )
    answer = messagebox.askyesnocancel("Покупка поля", msg)

    if answer is True:
        return "bonus"
    elif answer is False:
        return "normal"
    else:
        return None

def update_missions():
    if not missions_labels or not hasattr(model, "missions"):
        return

    m = model.missions

    def mark(done: bool):
        return ("●", "green") if done else ("●", "red")

    total = max(int(getattr(m, "total_fields", 0)), 0)
    opened = max(int(getattr(m, "unlocked_fields", 0)), 0)
    symbol, color = mark(getattr(m, "unlock_all_fields_done", False))
    missions_labels[0].config(
        text=f"{symbol} Відкрити всі поля: {opened}/{total}",
        fg=color
    )

    wheat = max(int(getattr(m, "wheat_count", 0)), 0)
    symbol, color = mark(getattr(m, "wheat_stock_done", False))
    missions_labels[1].config(
        text=f"{symbol} Стратегічний запас (пшениця): {wheat}/10",
        fg=color
    )

    money = max(int(getattr(m, "money", 0)), 0)
    symbol, color = mark(getattr(m, "save_1000_done", False))
    missions_labels[2].config(
        text=f"{symbol} Накопичити 1000 грошей: {money}/1000",
        fg=color
    )

    organic = max(int(getattr(m, "organic_plantings", 0)), 0)
    symbol, color = mark(getattr(m, "organic_done", False))
    missions_labels[3].config(
        text=f"{symbol} 10 посівів без добрив: {organic}/10",
        fg=color
    )

    longest = max(int(getattr(m, "longest_session_time", 0)), 0)
    current = max(int(getattr(m, "current_session_time", 0)), 0)
    symbol, color = mark(getattr(m, "longest_session_done", False))
    missions_labels[4].config(
        text=f"{symbol} Найдовша сесія: рекорд {longest} хв (зараз {current} хв)",
        fg=color
    )

    # місії від Родіона
    missions_labels[5].config(
        text="Місії від Родіона:",
        fg="black"
    )

    harvest = max(int(getattr(m, "total_harvest", 0)), 0)

    symbol, color = mark(m.first_harvest_done)
    missions_labels[6].config(
        text=f"{symbol} 'Перший урожай' Зберіть першу рослину: {harvest}/1",
        fg=color
    )

    symbol, color = mark(m.harvest_25_done)
    missions_labels[7].config(
        text=f"{symbol} 'Жатва' Зберіть 25 рослин: {harvest}/25",
        fg=color
    )

    symbol, color = mark(m.harvest_100_done)
    missions_labels[8].config(
        text=f"{symbol} 'Комбайн' Зберіть 100 рослин: {harvest}/100",
        fg=color
    )

    money = max(int(getattr(m, "money", 0)), 0)

    symbol, color = mark(m.trader_50_done)
    missions_labels[9].config(
        text=f"{symbol} 'Дрібний торговець' Заробіть 50₴ на продажу: {money}/50",
        fg=color
    )

    symbol, color = mark(m.trader_200_done)
    missions_labels[10].config(
        text=f"{symbol} 'Купець' Заробіть 200₴ на продажу: {money}/200",
        fg=color
    )

    symbol, color = mark(m.balance_500_done)
    missions_labels[11].config(
        text=f"{symbol} 'Золоті руки' Заробіть 500₴ на продажу: {money}/500",
        fg=color
    )


