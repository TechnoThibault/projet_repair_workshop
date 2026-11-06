from .customers_menu import CustomersMenu
from .menu import Menu


class MainMenu:
    """
    Menu shown to the user when the application launches.
    Allows the user to navigate between the different modules of the application.
    """

    def __init__(self, title: str):
        self.title = title
        self.menu_actions = {
            "0": {"description": "Close the application", "action": "close"},
            "1": {
                "description": "Customers",
                "action": lambda: CustomersMenu(
                    "Customers Menu"
                ),  # As the action is not a method in itself, needs to be called as a lambda
            },
        }
        Menu(self.title, self.menu_actions).get_choice()
