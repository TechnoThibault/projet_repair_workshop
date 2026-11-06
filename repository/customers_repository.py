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
                "SELECT p.id,p.first_name, p.last_name, p.phone_number, p.email, p.address, p.birth_date, p.created_at from customers c join persons p on c.person_id = p.id"
            )

            data = cursor.fetchall()
            customers = [Customer(*row) for row in data]

            return customers

    @classmethod
    def register_customer(cls, customer: Customer):
        with Database().connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO persons (first_name, last_name, phone_number, email, address, birth_date)
                VALUES(%s,%s,%s,%s,%s,%s)
                RETURNING ID
                """,
                (
                    customer.first_name,
                    customer.last_name,
                    customer.phone_number,
                    customer.email,
                    customer.address,
                    customer.birth_date,
                ),
            )
            person_id = cursor.fetchone()[0]

            cursor.execute(
                """
                INSERT INTO customers (person_id)
                VALUES(%s)
                RETURNING ID
                """,
                (person_id,),
            )

            customer_id = cursor.fetchone()[0]

            return customer_id

    @classmethod
    def update_customer(cls, customer: Customer):
        with Database().connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE PERSONS 
                SET 
                first_name = %s,
                last_name = %s,
                phone_number = %s,
                email = %s,
                address = %s,
                birth_date = %s
                WHERE id = %s
                """,
                (
                    customer.first_name,
                    customer.last_name,
                    customer.phone_number,
                    customer.email,
                    customer.address,
                    customer.birth_date,
                    customer.id,
                ),
            )

            rows_count = cursor.rowcount

            return rows_count
