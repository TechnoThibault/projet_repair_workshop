from db.database import Database
from models import Customer


class CustomersRepository:
    """
    Repository to access the database about the customers.
    """

    @classmethod
    def get_customers(cls):
        with Database().connection.cursor() as cursor:
            cursor.execute(
                "SELECT p.first_name, p.last_name, p.phone_number, p.email, p.address, p.birth_date, p.created_at from customers c join persons p on c.person_id = p.id"
            )

            data = cursor.fetchall()
            customers = [Customer(*row) for row in data]

            return customers
