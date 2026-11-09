from db.database import Database
from models import Customer


class CustomersRepository:
    """
    Repository to access the database about the customers.
    """

    @classmethod
    def get_customers(cls, person_id: bool = True):
        """Retrieve the list of all customers.

        Args:
            person_id (bool, optional): Decide if the ID shown will be that of the customer of the person linked to them. Defaults to True.

        Returns:
            list[Customer]: List of all the customers inside the database.
        """
        with Database().connection.cursor() as cursor:
            if person_id:

                cursor.execute(
                    "SELECT p.id,p.first_name, p.last_name, p.phone_number, p.email, p.address, p.birth_date, p.created_at from customers c join persons p on c.person_id = p.id"
                )
            else:
                cursor.execute(
                    "SELECT c.id,p.first_name, p.last_name, p.phone_number, p.email, p.address, p.birth_date, p.created_at from customers c join persons p on c.person_id = p.id"
                )

            data = cursor.fetchall()
            customers = [Customer(*row) for row in data]

            return customers

    @classmethod
    def register_customer(cls, customer: Customer):
        """Add a customer to the database.

        Args:
            customer (Customer) : Data about a customer.

        Returns:
            int: ID of the newly created customer.

        """
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
        """Update an existing customer with new values.

        Args:
            customer (Customer) : Data about a customer.

        Returns:
            int: number of rows updated.

        """
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

    @classmethod
    def delete_customer(cls, customer: Customer):
        """Delete an existing customer.

        Args:
            customer (Customer) : Data about a customer.

        Returns:
            int: number of rows updated.

        """
        with Database().connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM PERSONS
                WHERE id = %s
                """,
                (customer.id,),
            )

            rows_count = cursor.rowcount
            return rows_count
