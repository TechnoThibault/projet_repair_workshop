from datetime import datetime

import psycopg

from helpers import Helpers
from models import Technician
from repository import TechniciansRepository

from .menu import Menu


class TechniciansMenu:
    """
    Menu allowing users to search, consult, register, update, and delete
    technician records.

    Provides an interface to manage technician information, including
    personal details and contact information.
    """

    def __init__(self, title: str):
        """
        Initializes the technicians menu.

        Sets the menu title, defines the available actions, and launches
        the menu interface.

        Args:
            title (str): The title displayed at the top of the menu.
        """
        self.title = title
        self.menu_actions = {
            "0": {"description": "Close this menu", "action": "back"},
            "1": {
                "description": "Show all technicians",
                "action": self.show_technicians,
            },
            "2": {
                "description": "Register a new technician",
                "action": self.add_technician,
            },
            "3": {
                "description": "Update an existing technician",
                "action": self.update_technician,
            },
            "4": {
                "description": "Delete a technician",
                "action": self.delete_technician,
            },
        }
        Menu(self.title, self.menu_actions).get_choice()

    def show_technicians(self):
        """
        Retrieves and displays all registered technicians.

        Fetches technician records through the TechniciansRepository
        and displays their personal and contact information in a
        formatted table.

        If no technicians are found, displays an appropriate message.
        """
        technicians = TechniciansRepository.get_technicians()

        Helpers.header("TECHNICIANS")

        if not technicians:
            print("No technicians found.")
            return

        Helpers.display_table(
            headers=(
                "FIRST NAME",
                "LAST NAME",
                "PHONE NUMBER",
                "EMAIL",
                "ADDRESS",
                "BIRTH DATE",
                "CREATION DATE",
            ),
            rows=technicians,
            attributes=(
                "first_name",
                "last_name",
                "phone_number",
                "email",
                "address",
                "birth_date",
                "created_at",
            ),
        )

    def add_technician(self):
        """
        Registers a new technician in the database.

        Prompts the user to enter the technician's personal and contact
        information. Each input is validated before being accepted.

        Converts the birth date from DD/MM/YYYY format into a date object
        and constructs a Technician instance.

        Registers the technician through the TechniciansRepository.

        Handles unique constraint violations for email addresses
        and phone numbers by displaying an appropriate error message.
        """
        Helpers.header("REGISTER TECHNICIAN")
        print("Enter data concerning the user:")

        first_name = Helpers.get_validated_input(
            "First name: ", Technician.validate_first_name
        )

        last_name = Helpers.get_validated_input(
            "Last name: ", Technician.validate_last_name
        )

        phone_number = Helpers.get_validated_input(
            "Phone number: ", Technician.validate_phone_number
        )

        email = Helpers.get_validated_input("Email: ", Technician.validate_email)

        address = Helpers.get_validated_input("Address: ", Technician.validate_address)

        birth_date = Helpers.get_validated_input(
            "Birth date (DD/MM/YYYY): ", Technician.validate_birth_date
        )

        technician = Technician(
            0,
            first_name,
            last_name,
            phone_number,
            email,
            address,
            datetime.strptime(birth_date, "%d/%m/%Y").date(),
        )

        try:
            TechniciansRepository.register_technician(technician)

            print("Technician created.")
        # Emails and phone numbers are unique.
        except psycopg.errors.UniqueViolation as e:
            if e.diag.constraint_name == "persons_uk_email":
                print("This email address is already registered.")
            elif e.diag.constraint_name == "persons_uk_phone_number":
                print("This phone number is already registered.")

    def update_technician(self):
        """
        Updates the information of an existing technician.

        Retrieves and displays all registered technicians, then prompts
        the user to select one using its ID.

        Allows the user to modify each personal and contact information
        field individually. If an input is left empty, the existing
        value is retained.

        Validates the updated information and constructs a new
        Technician instance before sending it to the repository.

        Displays a success message if the update is successful,
        or an appropriate message if no record is updated.

        Handles unique constraint violations for email addresses
        and phone numbers.
        """
        Helpers.header("UPDATE TECHNICIAN")

        technicians = TechniciansRepository.get_technicians()

        ids = {technician.id for technician in technicians}

        if not technicians:
            print("No technicians found.")
            return

        Helpers.display_table(
            headers=(
                "ID",
                "FIRST NAME",
                "LAST NAME",
                "PHONE NUMBER",
                "EMAIL",
                "ADDRESS",
                "BIRTH DATE",
                "CREATION DATE",
            ),
            rows=technicians,
            attributes=(
                "id",
                "first_name",
                "last_name",
                "phone_number",
                "email",
                "address",
                "birth_date",
                "created_at",
            ),
        )

        while True:
            try:
                choice = int(input("Choose the technician to update: "))

                if choice in ids:
                    break

                print("Please choose a valid technician number.")

            except ValueError:
                print("You must enter a number.")

        technician = next(
            (technician for technician in technicians if technician.id == choice), None
        )

        if technician is None:
            print("There was an issue retrieving the technician.")
            return

        Helpers.header("TECHNICIAN INFORMATION")

        first_name = Helpers.get_optional_input(
            "First name",
            technician.first_name,
            Technician.validate_first_name,
        )

        last_name = Helpers.get_optional_input(
            "Last name",
            technician.last_name,
            Technician.validate_last_name,
        )

        phone_number = Helpers.get_optional_input(
            "Phone number",
            technician.phone_number,
            Technician.validate_phone_number,
        )

        email = Helpers.get_optional_input(
            "Email",
            technician.email,
            Technician.validate_email,
        )

        address = Helpers.get_optional_input(
            "Address",
            technician.address,
            Technician.validate_address,
        )

        birth_date = Helpers.get_optional_input(
            "Birth date (DD/MM/YYYY)",
            technician.birth_date.strftime("%d/%m/%Y"),
            Technician.validate_birth_date,
        )

        updated_technician = Technician(
            technician.id,
            first_name,
            last_name,
            phone_number,
            email,
            address,
            datetime.strptime(birth_date, "%d/%m/%Y").date(),
        )
        try:
            rows_count = TechniciansRepository.update_technician(updated_technician)
            if rows_count > 0:
                print("Technician updated successfully.")
            else:
                print("No technician updated.")
        except psycopg.errors.UniqueViolation as e:
            if e.diag.constraint_name == "persons_uk_email":
                print("This email address is already registered.")
            elif e.diag.constraint_name == "persons_uk_phone_number":
                print("This phone number is already registered.")

    def delete_technician(self):
        """
        Deletes an existing technician from the database.

        Retrieves and displays all registered technicians, then prompts
        the user to select the technician to delete using its ID.

        Displays the selected technician's information and requests
        confirmation before proceeding with the deletion.

        If the user cancels the operation, no changes are made.

        Calls the TechniciansRepository to delete the selected technician
        and displays an appropriate success or failure message.

        Handles database errors that may occur during deletion.
        """
        Helpers.header("DELETE TECHNICIAN")

        technicians = TechniciansRepository.get_technicians()

        ids = {technician.id for technician in technicians}

        if not technicians:
            print("No technicians found.")
            return

        Helpers.display_table(
            headers=(
                "ID",
                "FIRST NAME",
                "LAST NAME",
                "PHONE NUMBER",
                "EMAIL",
                "ADDRESS",
                "BIRTH DATE",
                "CREATION DATE",
            ),
            rows=technicians,
            attributes=(
                "id",
                "first_name",
                "last_name",
                "phone_number",
                "email",
                "address",
                "birth_date",
                "created_at",
            ),
        )

        while True:
            try:
                choice = int(input("Choose the technician to delete: "))

                if choice in ids:
                    break

                print("Please choose a valid technician number.")

            except ValueError:
                print("You must enter a number.")

        technician = next(
            (technician for technician in technicians if technician.id == choice), None
        )

        if technician is None:
            print("There was an issue retrieving the technician.")
            return

        choices = {"y", "n", ""}

        Helpers.header("TECHNICIAN INFORMATION")
        print(technician)

        while True:

            choice = input(
                "Are you sure you want to delete this technician? [y/N] "
            ).lower()

            if choice in choices:
                break

            print("Only valid choices are : 'y', 'n', ''.")

        if choice in ("n", ""):
            print("Deletion cancelled.")
            return

        try:
            rows_count = TechniciansRepository.delete_technician(technician)

            if rows_count > 0:
                print("Technician successfully deleted.")
            else:
                print("No technician has been deleted.")
        except psycopg.Error:
            print("There was an issue deleting the user.")

    def header(self, title: str):
        """
        Displays a formatted header in the terminal.

        Args:
            title (str): The title to display between separator lines.
        """
        print(f"\n=== {title} ===")
