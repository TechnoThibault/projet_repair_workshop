from repository.customers_repository import CustomersRepository

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
        }
        Menu(self.title, self.menu_actions).get_choice()

    def show_customers(self):
        customers = CustomersRepository.get_customers()

        print("\n=== CUSTOMERS ===")

        if not customers:
            print("No customers found.")
            return

        for customer in customers:
            print(customer)
