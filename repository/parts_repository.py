from db.database import Database
from models import Part


class PartsRepository:
    """
    Repository responsible for managing part records in the database.
    """

    @classmethod
    def get_parts(cls):
        """
        Retrieves all parts stored in the database.

        Returns:
            list[Part]: A list of Part instances representing all
                parts stored in the database.
        """
        with Database().connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, name, description, unit_price, stock_quantity, created_at, updated_at
                from parts
                """)

            data = cursor.fetchall()
            parts = [Part(*row) for row in data]

            return parts

    @classmethod
    def register_part(cls, part: Part):
        """
        Registers a new part in the database.

        Args:
            part (Part): The part instance containing the name,
                description, unit price, and stock quantity.

        Returns:
            int: The ID of the newly registered part.
        """
        with Database().connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO parts (name, description, unit_price, stock_quantity)
                VALUES(%s,%s,%s,%s)
                RETURNING ID
                """,
                (part.name, part.description, part.unit_price, part.stock_quantity),
            )
            part_id = cursor.fetchone()[0]

            return part_id

    @classmethod
    def update_part(cls, part: Part):
        """
        Updates an existing part in the database.

        Args:
            part (Part): The part instance containing the ID and the
                updated name, description, unit price, and stock quantity.

        Returns:
            int: The number of database rows affected by the update.
                Returns 0 if no matching part was found.
        """
        with Database().connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE parts 
                SET 
                name = %s,
                description = %s,
                unit_price = %s,
                stock_quantity = %s
                WHERE id = %s
                """,
                (
                    part.name,
                    part.description,
                    part.unit_price,
                    part.stock_quantity,
                    part.id,
                ),
            )

            rows_count = cursor.rowcount

            return rows_count

    @classmethod
    def delete_part(cls, part: Part):
        """
        Deletes an existing part from the database.

        Args:
            part (Part): The part instance containing the ID of
                the part to delete.

        Returns:
            int: The number of database rows affected by the deletion.
                Returns 0 if no matching part was found.
        """
        with Database().connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM parts
                WHERE id = %s
                """,
                (part.id,),
            )

            rows_count = cursor.rowcount
            return rows_count
