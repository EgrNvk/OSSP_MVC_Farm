from Model.model import FarmModel
from View import view
from Controller.controller import FarmController

def main():
    model = FarmModel()
    model.load_state()
    controller = FarmController(model)
    root = view.create_view(model, controller)
    root.mainloop()

if __name__ == "__main__":
    main()