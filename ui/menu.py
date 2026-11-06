import os

from helpers import Helpers


class Menu:
    """
    Reusable Menu object to show choices to the user and call different actions based on it.
    Each action will be ordered as defined in the menus and the action will be called from there.
    """

    def __init__(self, title: str, options: dict):
        self.title = title
        self.options = options

    def display(self):
        self.__clear_screen()
        Helpers.header(self.title)

        for key, value in self.options.items():
            print(f" {key}. {value['description']}")

    def get_choice(self):
        """
        Keep proposing choices to the user until they decide to leave the current menu or the application.
        The user needs to choose one of the options set by the application to go to the different menus.
        The action will be called based on the user's choice.
        """
        while True:
            self.display()

            choice = input("Choose an option: ")

            if choice not in self.options:
                print("Invalid choice!")
                input("Press Enter to continue...")
                continue

            action = self.options[choice]["action"]

            if action == "back":
                break

            if action == "close":
                print("Closing application...")
                break

            action()

            input("\nPress Enter to return to the menu...")

    def __clear_screen(self):
        """
        Allows the screen to be emptied.
        """
        os.system("cls" if os.name == "nt" else "clear")
