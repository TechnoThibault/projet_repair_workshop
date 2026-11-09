import psycopg

from helpers import Helpers
from models import Part
from repository import PartsRepository

from .menu import Menu


class PartsMenu:
    """
    Menu allowing users to search, modify, add, and delete part records.
    """

    def __init__(self, title: str):
        """
        Initializes the parts menu.

        Sets the menu title, defines the available actions, and displays
        the menu to allow users to manage parts.

        Args:
            title (str): The title displayed at the top of the menu.
        """
        self.title = title
        self.menu_actions = {
            "0": {"description": "Close this menu", "action": "back"},
            "1": {"description": "Show all parts", "action": self.show_parts},
            "2": {
                "description": "Register a new part",
                "action": self.add_part,
            },
            "3": {
                "description": "Update an existing part",
                "action": self.update_part,
            },
            "4": {"description": "Delete a part", "action": self.delete_part},
        }
        Menu(self.title, self.menu_actions).get_choice()

    def show_parts(self):
        """
        Displays all parts stored in the database.

        Retrieves the part records through the PartsRepository and
        displays them in a formatted table, including their names,
        descriptions, prices, stock quantities, and timestamps.

        If no parts are found, an informational message is displayed.
        """
        parts = PartsRepository.get_parts()

        Helpers.header("PARTS")

        if not parts:
            print("No parts found.")
            return

        Helpers.display_table(
            headers=(
                "NAME",
                "DESCRIPTION",
                "UNIT PRICE (€)",
                "STOCK",
                "CREATION DATE",
                "LAST UPDATE",
            ),
            rows=parts,
            attributes=(
                "name",
                "description",
                "unit_price",
                "stock_quantity",
                "created_at",
                "updated_at",
            ),
        )

    def add_part(self):
        """
        Registers a new part in the database.

        Prompts the user to enter the part's name, description, unit price,
        and stock quantity. Each input is validated before being used
        to construct a Part instance.

        Converts the unit price and stock quantity into their
        corresponding numeric types before registering the part.

        Handles database errors by displaying an appropriate message.
        """
        Helpers.header("REGISTER PART")
        print("Enter data concerning the part:")

        name = Helpers.get_validated_input("Name: ", Part.valid_name)

        description = Helpers.get_validated_input(
            "Description: ", Part.valid_description
        )

        unit_price = Helpers.get_validated_input("Unit price: ", Part.valid_unit_price)

        stock_quantity = Helpers.get_validated_input(
            "Stock quantity: ", Part.valid_stock_quantity
        )

        part = Part(0, name, description, float(unit_price), int(stock_quantity))

        try:
            PartsRepository.register_part(part)

            print("Part created.")
        # Emails and phone numbers are unique.
        except psycopg.Error as e:
            print(f"Error : {e}")

    def update_part(self):
        """
        Updates an existing part's information.

        Retrieves and displays all available parts, then prompts the user
        to select the part to update.

        Allows individual fields to be modified while retaining their
        existing values when an empty input is provided. Each new value
        is validated before being accepted.

        Converts the unit price and stock quantity into their
        corresponding numeric types before submitting the updated
        Part instance to the repository.

        Displays a success or failure message depending on the number
        of database rows affected. Handles database errors.
        """
        Helpers.header("UPDATE PART")

        parts = PartsRepository.get_parts()

        ids = {part.id for part in parts}

        if not parts:
            print("No parts found.")
            return

        Helpers.display_table(
            headers=(
                "ID",
                "NAME",
                "DESCRIPTION",
                "UNIT PRICE (€)",
                "STOCK",
                "CREATION DATE",
                "LAST UPDATE",
            ),
            rows=parts,
            attributes=(
                "id",
                "name",
                "description",
                "unit_price",
                "stock_quantity",
                "created_at",
                "updated_at",
            ),
        )

        while True:
            try:
                choice = int(input("Choose the part to update: "))

                if choice in ids:
                    break

                print("Please choose a valid part number.")

            except ValueError:
                print("You must enter a number.")

        part = next((part for part in parts if part.id == choice), None)

        if part is None:
            print("There was an issue retrieving the part.")
            return

        Helpers.header("PART INFORMATION")

        name = Helpers.get_optional_input(
            "Name",
            part.name,
            Part.valid_name,
        )

        description = Helpers.get_optional_input(
            "Description",
            part.description,
            Part.valid_description,
        )

        unit_price = Helpers.get_optional_input(
            "Unit price",
            part.unit_price,
            Part.valid_unit_price,
        )

        stock_quantity = Helpers.get_optional_input(
            "Stock quantity",
            part.stock_quantity,
            Part.valid_stock_quantity,
        )

        updated_part = Part(
            part.id,
            name,
            description,
            float(unit_price),
            int(stock_quantity),
        )
        try:
            rows_count = PartsRepository.update_part(updated_part)
            if rows_count > 0:
                print("Part updated successfully.")
            else:
                print("No part updated.")
        except psycopg.Error as e:
            print(f"Error : {e}")

    def delete_part(self):
        """
        Deletes an existing part from the database.

        Retrieves and displays all available parts, then prompts the user
        to select the part to delete.

        Displays the selected part's information and requests confirmation
        before proceeding with the deletion.

        Cancels the operation if the user declines or provides an
        empty response.

        Displays a success or failure message depending on the number
        of database rows affected. Handles database errors.
        """
        Helpers.header("DELETE PART")

        parts = PartsRepository.get_parts()

        ids = {part.id for part in parts}

        if not parts:
            print("No parts found.")
            return

        Helpers.display_table(
            headers=(
                "ID",
                "NAME",
                "DESCRIPTION",
                "UNIT PRICE (€)",
                "STOCK",
                "CREATION DATE",
                "LAST UPDATE",
            ),
            rows=parts,
            attributes=(
                "id",
                "name",
                "description",
                "unit_price",
                "stock_quantity",
                "created_at",
                "updated_at",
            ),
        )

        while True:
            try:
                choice = int(input("Choose the part to delete: "))

                if choice in ids:
                    break

                print("Please choose a valid part number.")

            except ValueError:
                print("You must enter a number.")

        part = next((part for part in parts if part.id == choice), None)

        if part is None:
            print("There was an issue retrieving the part.")
            return

        choices = {"y", "n", ""}

        Helpers.header("PART INFORMATION")
        print(part)

        while True:

            choice = input("Are you sure you want to delete this part? [y/N] ").lower()

            if choice in choices:
                break

            print("Only valid choices are : 'y', 'n', ''.")

        if choice in ("n", ""):
            print("Deletion cancelled.")
            return

        try:
            rows_count = PartsRepository.delete_part(part)

            if rows_count > 0:
                print("Part successfully deleted.")
            else:
                print("No part has been deleted.")
        except psycopg.Error:
            print("There was an issue deleting the user.")

    def header(self, title: str):
        """
        Displays a formatted section header.

        Args:
            title (str): The title to display between separator lines.
        """
        print(f"\n=== {title} ===")
