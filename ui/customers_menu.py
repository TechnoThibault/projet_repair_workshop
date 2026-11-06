from datetime import datetime

import psycopg

from helpers import Helpers
from models import Customer
from repository import CustomersRepository

from .menu import Menu


class CustomersMenu:
    """
    Menu allowing an user to search, modify, add or delete data about customers.
    """

    def __init__(self, title: str):
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
        }
        Menu(self.title, self.menu_actions).get_choice()

    def show_customers(self):
        """
        Show a list of all the customers to the user.
        """
        customers = CustomersRepository.get_customers()

        self.header("CUSTOMERS")

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
        Add a new customer to the database. Every input must be validated before being accepted.
        """
        self.header("REGISTER CUSTOMER")
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
            first_name,
            last_name,
            phone_number,
            email,
            address,
            datetime.strptime(birth_date, "%d/%m/%Y").date(),
        )

        try:
            CustomersRepository.register_customer(customer)

            print("Customercreated.")
        # Emails and phone numbers are unique.
        except psycopg.errors.UniqueViolation as e:
            if e.diag.constraint_name == "persons_uk_email":
                print("This email address is already registered.")
            elif e.diag.constraint_name == "persons_uk_phone_number":
                print("This phone number is already registered.")

    def update_customer(self):
        """
        Update an existing customer with new data. Each field can be modified, and if the user enters an empty string, the previous value will be used.
        """
        self.header("UPDATE CUSTOMER")

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

        self.header("CUSTOMER INFORMATION")

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

    def header(self, title: str):
        print(f"\n=== {title} ===")
