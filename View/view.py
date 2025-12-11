import tkinter as tk
from tkinter import messagebox
import json
from pathlib import Path

from Services.Resource_Service import ResourceService
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

field_buttons = []
field_labels = []

plant_var = None
fert_var = None
sell_var = None
sell_info_label = None


def create_view(app_model, app_controller):
    global root, model, controller
    global balance_label, ambar_label, warehouse_label
    global field_buttons, field_labels, plant_var, fert_var, sell_var, sell_info_label
    global current_images

    model = app_model
    controller = app_controller

    root = tk.Tk()
    root.title("Ферма")
    root.geometry("1000x1500")

    balance_label = tk.Label(root, font=("Arial", 16))
    balance_label.pack(pady=5)

    ambar_label = tk.Label(root, font=("Arial", 12))
    ambar_label.pack(pady=3)

    warehouse_label = tk.Label(root, font=("Arial", 12))
    warehouse_label.pack(pady=3)

    frame_select = tk.Frame(root, bd=2, relief="groove", padx=10, pady=10)
    frame_select.pack(pady=10)

    tk.Label(frame_select, text="Рослина:").grid(row=0, column=0, padx=5)
    plant_var = tk.StringVar(value=model.plants[0].name)
    tk.OptionMenu(frame_select, plant_var, *[p.name for p in model.plants]).grid(row=0, column=1)

    tk.Label(frame_select, text="Добриво:").grid(row=1, column=0, padx=5)
    fert_var = tk.StringVar(value="Без добрива")
    tk.OptionMenu(frame_select, fert_var, "Без добрива", *[f.name for f in model.fertilizers]).grid(row=1, column=1)

    frame_fields = tk.Frame(root, bd=2, relief="groove", padx=10, pady=10)
    frame_fields.pack(pady=10)

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

    frame_shop = tk.Frame(root, bd=2, relief="groove", padx=10, pady=10)
    frame_shop.pack()

    tk.Label(frame_shop, text="Магазин добрив").pack(anchor="w")

    for fert in model.fertilizers:
        tk.Button(
            frame_shop,
            text=f"Купити {fert.name} ({fert.price}₴)",
            command=lambda name=fert.name: on_buy_fertilizer(name)
        ).pack(anchor="w", pady=2)

    frame_sell = tk.Frame(root, bd=2, relief="groove", padx=10, pady=10)
    frame_sell.pack()

    tk.Label(frame_sell, text="Продаж").grid(row=0, column=0, columnspan=2)

    sell_var = tk.StringVar(value=model.plants[0].name)
    tk.OptionMenu(frame_sell, sell_var, *[p.name for p in model.plants]).grid(row=1, column=0)

    tk.Button(
        frame_sell,
        text="Продати 1 шт",
        command=on_sell_click
    ).grid(row=1, column=1)

    sell_info_label = tk.Label(frame_sell, text="", fg="gray")
    sell_info_label.grid(row=2, column=0, columnspan=2)

    update_all()

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

    for i, field in enumerate(model.fields):
        if not getattr(field, "unlocked", True):
            txt = f"Поле {i + 1}: заблоковано"
        elif field.state == "empty":
            txt = f"Поле {i + 1}: пусто"
        elif field.state == "growing":
            txt = f"Поле {i + 1}: росте"
        else:
            txt = f"Поле {i + 1}: ГОТОВО"

        field_labels[i].config(text=txt)

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
    messagebox.showwarning("Помилка", msg)