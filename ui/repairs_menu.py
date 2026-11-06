from helpers import Helpers
from models.enums import RepairStatus
from repository import RepairsRepository

from .menu import Menu


class RepairsMenu:
    """
    Menu allowing an user to search, modify, add or delete data about repairs.
    """

    def __init__(self, title: str):
        self.title = title
        self.menu_actions = {
            "0": {"description": "Close this menu", "action": "back"},
            "1": {
                "description": "Show repairs",
                "action": self.show_repairs,
            },
            "2": {
                "description": "Show data about a repair",
                "action": self.show_repair,
            },
        }
        Menu(self.title, self.menu_actions).get_choice()

    def show_repairs(self):
        """
        Show a list of all the repairs to the user.
        """

        Helpers.header("REPAIRS")

        statuses = [status.value for status in RepairStatus]

        for i, status in enumerate(statuses):
            print(f"{i+1:>3}. {status.capitalize().replace("_"," ")}")

        while True:
            try:

                choice = input("Choose the type of repair to show (default: all): ")

                if choice == "" or 1 <= int(choice) <= len(statuses):
                    break

                print(
                    "You must either enter an empty string or an integer from the list."
                )
            except ValueError:
                print(
                    "You must either enter an empty string or an integer from the list."
                )

        if choice == "":
            repairs = RepairsRepository.get_repairs()
        else:
            repairs = RepairsRepository.get_repairs(statuses[int(choice) - 1])

        Helpers.display_table(
            ("DESCRIPTION", "STATUS", "LABOR COST (€)", "CREATION DATE", "LAST UPDATE"),
            repairs,
            ("description", "status", "labor_cost", "created_at", "updated_at"),
        )

    def show_repair(self):
        Helpers.header("REPAIR")
        statuses = [status.value for status in RepairStatus]

        for i, status in enumerate(statuses):
            print(f"{i+1:>3}. {status.capitalize().replace("_"," ")}")

        while True:
            try:

                choice = input("Choose the type of repair to show (default: all): ")

                if choice == "" or 1 <= int(choice) <= len(statuses):
                    break

                print(
                    "You must either enter an empty string or an integer from the list."
                )
            except ValueError:
                print(
                    "You must either enter an empty string or an integer from the list."
                )

        if choice == "":
            repairs = RepairsRepository.get_repairs()
        else:
            repairs = RepairsRepository.get_repairs(statuses[int(choice) - 1])

        ids = [repair.id for repair in repairs]

        Helpers.display_table(
            (
                "ID",
                "DESCRIPTION",
                "STATUS",
                "LABOR COST (€)",
                "CREATION DATE",
                "LAST UPDATE",
            ),
            repairs,
            ("id", "description", "status", "labor_cost", "created_at", "updated_at"),
        )

        while True:
            try:
                choice = int(input("Enter the ID of the repair you wish to consult: "))

                if choice in ids:
                    break

                print("The ID must be in the list above.")

            except ValueError:
                print("You must enter a number.")

        repair = next((repair for repair in repairs if repair.id == choice), None)

        if repair is None:
            print("There was an issue recovering the repair.")
            return

        print(repair)
