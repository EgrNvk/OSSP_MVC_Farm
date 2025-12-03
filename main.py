from model import FarmModel
import view
from controller import FarmController

def main():
    model = FarmModel()
    controller = FarmController(model)
    root = view.create_view(model, controller)
    root.mainloop()

if __name__ == "__main__":
    main()