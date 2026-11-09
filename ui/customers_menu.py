from datetime import datetime

import psycopg

from helpers import Helpers
from models import Customer
from repository import CustomersRepository

from .menu import Menu


class CustomersMenu:
    """
    Menu allowing users to search, modify, add, and delete customer records.
    """

    def __init__(self, title: str):
        """
        Initializes the customers menu.

        Sets the menu title, defines the available actions, and displays
        the menu to allow users to manage customer records.

        Args:
            title (str): The title displayed at the top of the menu.
        """
        self.title = title
        self.menu_actions = {
            "0": {"description": "Close this menu", "action": "back"},
            "1": {"description": "Show all customers", "action": self.show_customers},
            "2": {
                "description": "Register a new customer",
                "action": self.add_customer,
            },
            "3": {
                "description": "Update an existing customer",
                "action": self.update_customer,
            },
            "4": {"description": "Delete a customer", "action": self.delete_customer},
        }
        Menu(self.title, self.menu_actions).get_choice()

    def show_customers(self):
        """
        Displays all customers stored in the database.

        Retrieves the customer records through the CustomersRepository
        and displays them in a formatted table. If no customers are found,
        an informational message is displayed.
        """
        customers = CustomersRepository.get_customers()

        Helpers.header("CUSTOMERS")

        if not customers:
            print("No customers found.")
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
            rows=customers,
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

    def add_customer(self):
        """
        Registers a new customer in the database.

        Prompts the user to enter the customer's personal information.
        Each input is validated before being used to construct a Customer
        instance.

        Converts the birth date from DD/MM/YYYY format into a date object
        before registering the customer.

        Handles unique constraint violations for email addresses and
        phone numbers by displaying an appropriate error message.
        """
        Helpers.header("REGISTER CUSTOMER")
        print("Enter data concerning the user:")

        first_name = Helpers.get_validated_input(
            "First name: ", Customer.validate_first_name
        )

        last_name = Helpers.get_validated_input(
            "Last name: ", Customer.validate_last_name
        )

        phone_number = Helpers.get_validated_input(
            "Phone number: ", Customer.validate_phone_number
        )

        email = Helpers.get_validated_input("Email: ", Customer.validate_email)

        address = Helpers.get_validated_input("Address: ", Customer.validate_address)

        birth_date = Helpers.get_validated_input(
            "Birth date (DD/MM/YYYY): ", Customer.validate_birth_date
        )

        customer = Customer(
            0,
            first_name,
            last_name,
            phone_number,
            email,
            address,
            datetime.strptime(birth_date, "%d/%m/%Y").date(),
        )

        try:
            CustomersRepository.register_customer(customer)

            print("Customer created.")
        # Emails and phone numbers are unique.
        except psycopg.errors.UniqueViolation as e:
            if e.diag.constraint_name == "persons_uk_email":
                print("This email address is already registered.")
            elif e.diag.constraint_name == "persons_uk_phone_number":
                print("This phone number is already registered.")

    def update_customer(self):
        """
        Updates an existing customer's information.

        Retrieves and displays all customers, then prompts the user
        to select the customer to update.

        Allows the user to modify individual fields while retaining
        their existing values when an empty input is provided.
        Each new value is validated before being accepted.

        Converts the birth date into a date object and submits the
        updated Customer instance to the repository.

        Handles unique constraint violations for email addresses
        and phone numbers and displays the corresponding messages.
        """
        Helpers.header("UPDATE CUSTOMER")

        customers = CustomersRepository.get_customers()

        ids = {customer.id for customer in customers}

        if not customers:
            print("No customers found.")
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
            rows=customers,
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
                choice = int(input("Choose the customer to update: "))

                if choice in ids:
                    break

                print("Please choose a valid customer number.")

            except ValueError:
                print("You must enter a number.")

        customer = next(
            (customer for customer in customers if customer.id == choice), None
        )

        if customer is None:
            print("There was an issue retrieving the customer.")
            return

        Helpers.header("CUSTOMER INFORMATION")

        first_name = Helpers.get_optional_input(
            "First name",
            customer.first_name,
            Customer.validate_first_name,
        )

        last_name = Helpers.get_optional_input(
            "Last name",
            customer.last_name,
            Customer.validate_last_name,
        )

        phone_number = Helpers.get_optional_input(
            "Phone number",
            customer.phone_number,
            Customer.validate_phone_number,
        )

        email = Helpers.get_optional_input(
            "Email",
            customer.email,
            Customer.validate_email,
        )

        address = Helpers.get_optional_input(
            "Address",
            customer.address,
            Customer.validate_address,
        )

        birth_date = Helpers.get_optional_input(
            "Birth date (DD/MM/YYYY)",
            customer.birth_date.strftime("%d/%m/%Y"),
            Customer.validate_birth_date,
        )

        updated_customer = Customer(
            customer.id,
            first_name,
            last_name,
            phone_number,
            email,
            address,
            datetime.strptime(birth_date, "%d/%m/%Y").date(),
        )
        try:
            rows_count = CustomersRepository.update_customer(updated_customer)
            if rows_count > 0:
                print("Customer updated successfully.")
            else:
                print("No customer updated.")
        except psycopg.errors.UniqueViolation as e:
            if e.diag.constraint_name == "persons_uk_email":
                print("This email address is already registered.")
            elif e.diag.constraint_name == "persons_uk_phone_number":
                print("This phone number is already registered.")

    def delete_customer(self):
        """
        Deletes an existing customer from the database.

        Retrieves and displays all customers, then prompts the user
        to select the customer to delete.

        Displays the selected customer's information and requests
        confirmation before proceeding with the deletion.

        Cancels the operation if the user declines or provides an
        empty response.

        Handles database errors and displays an appropriate message
        if the deletion cannot be completed.
        """
        Helpers.header("DELETE CUSTOMER")

        customers = CustomersRepository.get_customers()

        ids = {customer.id for customer in customers}

        if not customers:
            print("No customers found.")
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
            rows=customers,
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
                choice = int(input("Choose the customer to delete: "))

                if choice in ids:
                    break

                print("Please choose a valid customer number.")

            except ValueError:
                print("You must enter a number.")

        customer = next(
            (customer for customer in customers if customer.id == choice), None
        )

        if customer is None:
            print("There was an issue retrieving the customer.")
            return

        choices = {"y", "n", ""}

        Helpers.header("CUSTOMER INFORMATION")
        print(customer)

        while True:

            choice = input(
                "Are you sure you want to delete this customer? [y/N] "
            ).lower()

            if choice in choices:
                break

            print("Only valid choices are : 'y', 'n', ''.")

        if choice in ("n", ""):
            print("Deletion cancelled.")
            return

        try:
            rows_count = CustomersRepository.delete_customer(customer)

            if rows_count > 0:
                print("Customer successfully deleted.")
            else:
                print("No customer has been deleted.")
        except psycopg.Error:
            print("There was an issue deleting the user.")
