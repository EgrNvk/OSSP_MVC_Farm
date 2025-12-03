import tkinter as tk
from tkinter import messagebox

root = None
model = None
controller = None

balance_label = None
ambar_label = None
warehouse_label = None
field_buttons = []

plant_var = None
fert_var = None
sell_var = None
sell_info_label = None


def create_view(app_model, app_controller):
    global root, model, controller
    global balance_label, ambar_label, warehouse_label
    global field_buttons, plant_var, fert_var, sell_var, sell_info_label

    model = app_model
    controller = app_controller

    root = tk.Tk()
    root.title("Ферма")
    root.geometry("800x600")

    balance_label = tk.Label(root, font=("Arial", 16))
    balance_label.pack(pady=5)

    ambar_label = tk.Label(root, font=("Arial", 12))
    ambar_label.pack(pady=3)

    warehouse_label = tk.Label(root, font=("Arial", 12))
    warehouse_label.pack(pady=3)

    frame_select = tk.Frame(root, bd=2, relief="groove", padx=10, pady=10)
    frame_select.pack(pady=10)

    tk.Label(frame_select, text="Рослина:").grid(row=0, column=0, padx=5, pady=5)
    plant_names = [p.name for p in model.plants]
    plant_var = tk.StringVar(value=plant_names[0])
    tk.OptionMenu(frame_select, plant_var, *plant_names).grid(row=0, column=1)

    tk.Label(frame_select, text="Добриво:").grid(row=1, column=0, padx=5, pady=5)
    fert_names = ["Без добрива"] + [f.name for f in model.fertilizers]
    fert_var = tk.StringVar(value=fert_names[0])
    tk.OptionMenu(frame_select, fert_var, *fert_names).grid(row=1, column=1)

    frame_fields = tk.Frame(root, bd=2, relief="groove", padx=10, pady=10)
    frame_fields.pack(pady=10)

    tk.Label(frame_fields, text="Поля ферми").grid(row=0, column=0, columnspan=4)

    field_buttons = []
    for i in range(len(model.fields)):
        btn = tk.Button(
            frame_fields,
            text=f"Поле {i+1}: пусто",
            width=20,
            command=lambda idx=i: on_field_click(idx)
        )
        btn.grid(row=1, column=i, padx=10, pady=10)
        field_buttons.append(btn)

    frame_shop = tk.Frame(root, bd=2, relief="groove", padx=10, pady=10)
    frame_shop.pack(pady=10)

    tk.Label(frame_shop, text="Магазин добрив").grid(row=0, column=0, sticky="w")

    for i, fert in enumerate(model.fertilizers):
        tk.Button(
            frame_shop,
            text=f"Купити: {fert.name} ({fert.price}₴)",
            command=lambda name=fert.name: on_buy_fertilizer(name)
        ).grid(row=i + 1, column=0, sticky="w", pady=2)

    frame_sell = tk.Frame(root, bd=2, relief="groove", padx=10, pady=10)
    frame_sell.pack(pady=10)

    tk.Label(frame_sell, text="Продаж урожаю").grid(row=0, column=0, columnspan=2)

    sell_var = tk.StringVar(value=plant_names[0])
    tk.OptionMenu(frame_sell, sell_var, *plant_names).grid(row=1, column=0)

    tk.Button(
        frame_sell,
        text="Продати 1 шт",
        command=on_sell_click
    ).grid(row=1, column=1)

    sell_info_label = tk.Label(frame_sell, text="", fg="gray")
    sell_info_label.grid(row=2, column=0, columnspan=2)

    update_all()
    return root


def on_buy_fertilizer(fert_name):
    controller.buy_fertilizer(fert_name)


def on_field_click(field_index):
    controller.field_clicked(field_index)


def on_sell_click():
    controller.sell_crop(sell_var.get())


def update_balance():
    balance_label.config(text=f"Баланс: {model.balance}₴")


def update_ambar():
    text = ", ".join([f"{name}: {qty}" for name, qty in model.ambar.items()])
    ambar_label.config(text="Амбар: " + text)


def update_warehouse():
    text = ", ".join([f"{name}: {qty}" for name, qty in model.warehouse.items()])
    warehouse_label.config(text="Склад добрив: " + text)


def update_field(index, text):
    field_buttons[index].config(text=text)


def update_sell_info(text):
    sell_info_label.config(text=text)


def update_all():
    update_balance()
    update_ambar()
    update_warehouse()

    for i, field in enumerate(model.fields):
        if field.state == "empty":
            txt = f"Поле {i+1}: пусто"
        elif field.state == "growing":
            txt = f"Поле {i+1}: росте {field.plant.name}"
        elif field.state == "ready":
            txt = f"Поле {i+1}: {field.plant.name} ГОТОВЕ"
        update_field(i, txt)


def show_warning(msg):
    messagebox.showwarning("Помилка", msg)
