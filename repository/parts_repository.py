from db.database import Database
from models import Part


class PartsRepository:
    """
    Repository to access the database about the parts.
    """

    @classmethod
    def get_parts(cls):
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
