import os

from helpers import Helpers


class Menu:
    """
    Reusable menu component responsible for displaying options and
    executing the corresponding actions based on user input.

    Provides a consistent navigation mechanism across the application,
    allowing users to navigate between menus or close the application.
    """

    def __init__(self, title: str, options: dict):
        """
        Initializes a menu with a title and a collection of available options.

        Args:
            title (str): The title displayed at the top of the menu.
            options (dict): A dictionary containing the available menu options.
                Each entry must contain a description and an associated action.
        """
        self.title = title
        self.options = options

    def display(self):
        """
        Displays the menu and its available options.

        Clears the terminal screen, displays the menu title, and prints
        each option with its corresponding description.
        """
        self.__clear_screen()
        Helpers.header(self.title)

        for key, value in self.options.items():
            print(f" {key}. {value['description']}")

    def get_choice(self):
        """
        Handles user navigation through the menu.

        Continuously displays the menu and prompts the user to select
        an available option.

        Executes the corresponding action when a valid option is selected.
        Invalid choices are rejected and the user is prompted again.

        Terminates the menu loop when the user selects the back or close
        action. After executing an action, waits for user confirmation
        before displaying the menu again.
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
        Clears the terminal screen.

        Uses the appropriate system command depending on the operating
        system:
            - Windows: cls
            - Linux and macOS: clear
        """
        os.system("cls" if os.name == "nt" else "clear")
