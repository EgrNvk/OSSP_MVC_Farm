import tkinter as tk
from tkinter import messagebox
import json
from pathlib import Path

RESOURCES_FILE = Path(__file__).parent.parent/("resources.json")

with open(RESOURCES_FILE, "r", encoding="utf-8") as f:
    RES=json.load(f)

IMAGE_FOLDERS=RES.get("image_folders", {})

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

    model = app_model
    controller = app_controller

    root = tk.Tk()
    root.title("Ферма")
    root.geometry("1000x705")

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

    btn_field1 = tk.Button(
        frame_fields,
        text="",
        width=100,
        height=200,
        compound="top",
        command=lambda: on_field_click(0)
    )
    btn_field1.grid(row=0, column=0, padx=20, pady=5)
    field_buttons.append(btn_field1)

    lbl_field1 = tk.Label(frame_fields, text="Поле 1: пусто")
    lbl_field1.grid(row=1, column=0, padx=20, pady=5)
    field_labels.append(lbl_field1)

    btn_field2 = tk.Button(
        frame_fields,
        text="",
        width=100,
        height=200,
        compound="top",
        command=lambda: on_field_click(1)
    )
    btn_field2.grid(row=0, column=1, padx=20, pady=5)
    field_buttons.append(btn_field2)

    lbl_field2 = tk.Label(frame_fields, text="Поле 2: пусто")
    lbl_field2.grid(row=1, column=1, padx=20, pady=5)
    field_labels.append(lbl_field2)

    btn_field3 = tk.Button(
        frame_fields,
        text="",
        width=100,
        height=200,
        compound="top",
        command=lambda: on_field_click(2)
    )
    btn_field3.grid(row=0, column=2, padx=20, pady=5)
    field_buttons.append(btn_field3)

    lbl_field3 = tk.Label(frame_fields, text="Поле 3: пусто")
    lbl_field3.grid(row=1, column=2, padx=20, pady=5)
    field_labels.append(lbl_field3)

    btn_field4 = tk.Button(
        frame_fields,
        text="",
        width=100,
        height=200,
        compound="top",
        command=lambda: on_field_click(3)
    )
    btn_field4.grid(row=0, column=3, padx=20, pady=5)
    field_buttons.append(btn_field4)

    lbl_field4 = tk.Label(frame_fields, text="Поле 4: пусто")
    lbl_field4.grid(row=1, column=3, padx=20, pady=5)
    field_labels.append(lbl_field4)

    for i in range(4):
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

    if field.plant is None:
        folder = IMAGE_FOLDERS.get("empty", "IMG_carrot")
    else:
        folder = IMAGE_FOLDERS.get(field.plant.name)

        if not folder:
            folder=getattr(field.plant, "image_folder", None)

        if not folder:
            folder="IMG_carrot"

    path=f"{folder}/{stage}.png"

    try:
        img = tk.PhotoImage(file=path)
    except Exception as e:
        print(f"[WARN] Can't load image: {path} ({e})")
        return

    btn = field_buttons[index]
    btn.image = img
    btn.config(image=img)


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
        if field.state == "empty":
            txt = f"Поле {i+1}: пусто"
        elif field.state == "growing":
            txt = f"Поле {i+1}: росте"
        else:
            txt = f"Поле {i+1}:ГОТОВО"
        field_labels[i].config(text=txt)


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