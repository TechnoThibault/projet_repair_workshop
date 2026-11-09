from datetime import datetime

import psycopg

from helpers import Helpers
from models import Customer, Device, Repair, RepairStatus
from models.repair_comment import RepairComment
from models.repair_part import RepairPart
from repository import (
    CustomersRepository,
    DevicesRepository,
    PartsRepository,
    RepairCommentsRepository,
    RepairPartsRepository,
    RepairsRepository,
    TechniciansRepository,
)

from .menu import Menu


class RepairsMenu:
    """
    Menu allowing a user to search, modify, add or delete data about repairs.
    """

    def __init__(self, title: str):
        self.title = title
        self.menu_actions = {
            "0": {"description": "Close this menu", "action": "back"},
            "1": {"description": "Show repairs", "action": self.show_repairs},
            "2": {
                "description": "Show data about a repair",
                "action": self.show_repair,
            },
            "3": {
                "description": "Create a repair request",
                "action": self.create_repair,
            },
            "4": {
                "description": "Add comment to a repair request",
                "action": self.add_comment,
            },
            "5": {
                "description": "Add a part to a repair request",
                "action": self.add_repair_part,
            },
        }

        Menu(self.title, self.menu_actions).get_choice()

    def _get_repair_status(self):
        statuses = [status.value for status in RepairStatus]

        for i, status in enumerate(statuses):
            print(f"{i + 1:>3}. {status.capitalize().replace('_', ' ')}")

        while True:
            choice = input("Choose the type of repair to show (default: all): ")

            if choice == "":
                return None

            try:
                choice = int(choice)

                if 1 <= choice <= len(statuses):
                    return statuses[choice - 1]

            except ValueError:
                pass

            print("You must either enter an empty string or an integer from the list.")

    def show_repairs(self):
        """Show a list of all repairs, optionally filtered by status."""

        Helpers.header("REPAIRS")

        status = self._get_repair_status()
        repairs = RepairsRepository.get_repairs(status)

        Helpers.display_table(
            ("DESCRIPTION", "STATUS", "LABOR COST (€)", "CREATION DATE", "LAST UPDATE"),
            repairs,
            ("description", "status", "labor_cost", "created_at", "updated_at"),
        )

    def show_repair(self):
        """Display and consult a specific repair."""

        Helpers.header("REPAIR")

        status = self._get_repair_status()
        repairs = RepairsRepository.get_repairs(status)

        if not repairs:
            print("No repairs found.")
            return

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

        repair: Repair = self._select_repair(repairs)

        comments = RepairCommentsRepository.get_repair_comments(repair.id)

        for comment in comments:
            repair.add_comment(comment)

        repair_parts = RepairPartsRepository.get_repair_parts(repair.id)

        for repair_part in repair_parts:
            repair.add_part(repair_part)

        if repair is not None:
            print(repair)

    def _select_repair(self, repairs):
        ids = {repair.id for repair in repairs}

        while True:
            try:
                choice = int(input("Enter the ID of the repair you wish to consult: "))

                if choice in ids:
                    return next(repair for repair in repairs if repair.id == choice)

                print("The ID must be in the list above.")

            except ValueError:
                print("You must enter a number.")

    def _get_customer(self):
        choices = ("y", "n", "")

        while True:
            choice = input("Do you wish to use an existing customer? [y/N] ").lower()

            if choice in choices:
                break

            print("Only valid choices are: 'y', 'n', ''.")

        if choice == "y":
            customer = self._get_existing_customer()

            if customer is not None:
                return customer

        return self._create_customer()

    def _get_existing_customer(self):
        customers = CustomersRepository.get_customers(False)

        if not customers:
            print("No customers found, you have to create one.")
            return None

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

        ids = {customer.id for customer in customers}

        while True:
            try:
                choice = int(input("Choose the customer to use: "))

                if choice in ids:
                    return next(
                        customer for customer in customers if customer.id == choice
                    )

                print("Please choose a valid customer number.")

            except ValueError:
                print("You must enter a number.")

    def _create_customer(self):
        while True:
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

            address = Helpers.get_validated_input(
                "Address: ", Customer.validate_address
            )

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
                customer.id = CustomersRepository.register_customer(customer)
                print("Customer created.")
                return customer

            except psycopg.errors.UniqueViolation as e:
                if e.diag.constraint_name == "persons_uk_email":
                    print("This email address is already registered.")

                elif e.diag.constraint_name == "persons_uk_phone_number":
                    print("This phone number is already registered.")

                else:
                    raise

    def _create_device(self, customer):
        print("Enter the data used for the device:")

        brand = Helpers.get_validated_input("Brand: ", Device.validate_brand)

        model = Helpers.get_validated_input("Model: ", Device.validate_model)

        serial_number = Helpers.get_validated_input(
            "Serial number: ", Device.validate_serial_number
        )

        device_type = Helpers.get_validated_input(
            "Device type: ", Device.validate_device_type
        )

        device = Device(
            0,
            customer,
            brand,
            model,
            serial_number,
            device_type,
        )

        device.id = DevicesRepository.register_device(device)

        return device

    def _get_technician(self):
        while True:
            choice = input(
                "Do you want to assign a technician to the repair? [y/N] "
            ).lower()

            if choice in ("y", "n", ""):
                break

            print("Only choices are: 'y', 'n', ''.")

        if choice != "y":
            return None

        technicians = TechniciansRepository.get_technicians(False)

        if not technicians:
            print("No technicians found.")
            return None

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

        ids = {technician.id for technician in technicians}

        while True:
            try:
                choice = int(input("Choose the technician to assign: "))

                if choice in ids:
                    return next(
                        technician
                        for technician in technicians
                        if technician.id == choice
                    )

                print("Please choose a valid technician number.")

            except ValueError:
                print("You must enter a number.")

    def _create_repair_request(self, device, technician):
        print("Enter data concerning the repair:")

        description = Helpers.get_validated_input(
            "Description: ", Repair.validate_description
        )

        labor_cost = Helpers.get_validated_input(
            "Labor cost: ", Repair.valid_labor_cost
        )

        repair = Repair(
            0,
            device=device,
            description=description,
            status=RepairStatus.PENDING.value,
            labor_cost=float(labor_cost),
            technician=technician,
        )

        try:
            RepairsRepository.add_repair(repair)
            print("Repair request created.")

        except psycopg.Error as e:
            print(f"Error: {e}")

    def create_repair(self):

        Helpers.header("CREATE NEW REPAIR")

        separator = "*" * 50
        print(separator)

        customer = self._get_customer()

        print(separator)
        device = self._create_device(customer)

        print(separator)
        technician = self._get_technician()

        print(separator)
        self._create_repair_request(device, technician)

    def add_comment(self):
        Helpers.header("ADD COMMENT TO REPAIR")

        Helpers.header("REPAIRS")

        status = self._get_repair_status()
        repairs = RepairsRepository.get_repairs(status)

        if not repairs:
            print("No repairs found.")
            return

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

        repair = self._select_repair(repairs)
        if repair is None:
            print("There was an issue retrieving the repair request.")
            return
        print(repair)

        choices = ("y", "n", "")

        while True:
            choice = input(
                "Do you wish to add a comment to this repair? [Y/n] "
            ).lower()

            if choice in choices:
                break

            print("Only valid choices are: 'y', 'n', ''.")

        if choice == "n":
            print("Comment cancelled.")
            return

        technicians = TechniciansRepository.get_technicians(False)

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
                choice = int(input("Choose the technician the comment is linked to: "))

                if choice in ids:
                    break

                print("Please choose a valid technician number.")

            except ValueError:
                print("You must enter a number.")

        technician = next(
            (technician for technician in technicians if technician.id == choice), None
        )

        comment = Helpers.get_validated_input(
            "Comment: ", RepairComment.validate_comment
        )

        repair_comment = RepairComment(0, comment, technician)
        try:
            RepairCommentsRepository.add_repair_comment(repair_comment, repair)

            print("Repair comment added.")
        except psycopg.Error as e:
            print(f"Error: {e}")

    def add_repair_part(self):
        """Add a part to an existing repair."""

        Helpers.header("ADD PART TO REPAIR")

        repairs = RepairsRepository.get_repairs(None)

        if not repairs:
            print("No repairs found.")
            return

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

        repair = self._select_repair(repairs)

        if repair is None:
            print("There was an issue retrieving the repair.")
            return

        print(f"\nSelected repair: {repair}")

        parts = PartsRepository.get_parts()

        if not parts:
            print("No parts available.")
            return

        available_parts = [part for part in parts if part.stock_quantity > 0]

        if not available_parts:
            print("No parts available in stock.")
            return

        Helpers.display_table(
            (
                "ID",
                "NAME",
                "DESCRIPTION",
                "UNIT PRICE (€)",
                "STOCK",
            ),
            available_parts,
            (
                "id",
                "name",
                "description",
                "unit_price",
                "stock_quantity",
            ),
        )

        part_ids = {part.id for part in available_parts}

        while True:
            try:
                choice = int(input("Choose the part to add: "))

                if choice in part_ids:
                    part = next(part for part in available_parts if part.id == choice)
                    break

                print("Please choose a valid part ID.")

            except ValueError:
                print("You must enter a number.")

        while True:
            try:
                quantity = int(input("Enter the quantity: "))

                if quantity <= 0:
                    print("Quantity must be greater than zero.")
                    continue

                if quantity > part.stock_quantity:
                    print(
                        f"Not enough stock. Available quantity: "
                        f"{part.stock_quantity}"
                    )
                    continue

                break

            except ValueError:
                print("You must enter a valid integer.")

        repair_part = RepairPart(
            id=0,
            part=part,
            quantity=quantity,
            unit_price=part.unit_price,
        )

        try:
            RepairPartsRepository.add_repair_part(
                repair_part,
                repair,
            )

            print("\nPart successfully added to repair.")

            print(repair_part)

        except psycopg.Error as e:
            print(f"Error while adding part: {e}")
