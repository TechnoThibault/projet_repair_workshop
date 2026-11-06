from datetime import datetime

import psycopg

from helpers import Helpers
from models import Technician
from repository import TechniciansRepository

from .menu import Menu


class TechniciansMenu:
    """
    Menu allowing an user to search, modify, add or delete data about technicians.
    """

    def __init__(self, title: str):
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
        Show a list of all the technicians to the user.
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
        Add a new technician to the database. Every input must be validated before being accepted.
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
        Update an existing technician with new data. Each field can be modified, and if the user enters an empty string, the previous value will be used.
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
        Delete a technician from the database based on its id. Demands confirmation from the user before  commiting.
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
        print(f"\n=== {title} ===")
