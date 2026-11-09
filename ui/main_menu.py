from .customers_menu import CustomersMenu
from .menu import Menu
from .parts_menu import PartsMenu
from .repairs_menu import RepairsMenu
from .technicians_menu import TechniciansMenu


class MainMenu:
    """
    Main menu displayed when the application starts.

    Provides navigation to the different modules of the application,
    allowing users to manage customers, technicians, parts, and repairs,
    or close the application.
    """

    def __init__(self, title: str):
        """
        Initializes and displays the main application menu.

        Sets the menu title, defines the available actions, and associates
        each menu option with the corresponding submenu or application
        closing action.

        Submenus are instantiated through lambda functions to ensure
        they are only created when the corresponding option is selected.

        Args:
            title (str): The title displayed at the top of the main menu.
        """
        self.title = title
        self.menu_actions = {
            "0": {"description": "Close the application", "action": "close"},
            "1": {
                "description": "Customers",
                "action": lambda: CustomersMenu(
                    "Customers Menu"
                ),  # As the action is not a method in itself, needs to be called as a lambda
            },
            "2": {
                "description": "Technicians",
                "action": lambda: TechniciansMenu("Technicians Menu"),
            },
            "3": {
                "description": "Parts",
                "action": lambda: PartsMenu("Parts Menu"),
            },
            "4": {
                "description": "Repairs",
                "action": lambda: RepairsMenu("Repairs Menu"),
            },
        }
        Menu(self.title, self.menu_actions).get_choice()
