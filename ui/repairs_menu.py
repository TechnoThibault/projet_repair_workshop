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

    #     class RepairStatus(Enum):
    # PENDING = "pending"
    # IN_PROGRESS = "in_progress"
    # WAITING_FOR_PARTS = "waiting_for_parts"
    # COMPLETED = "completed"
    # CANCELLED = "cancelled"
