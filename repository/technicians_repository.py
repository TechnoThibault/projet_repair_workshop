from db.database import Database
from models import Technician


class TechniciansRepository:
    """
    Repository to access the database about the technicians.
    """

    @classmethod
    def get_technicians(cls):
        with Database().connection.cursor() as cursor:
            cursor.execute(
                "SELECT p.id,p.first_name, p.last_name, p.phone_number, p.email, p.address, p.birth_date, p.created_at from technicians t join persons p on t.person_id = p.id"
            )

            data = cursor.fetchall()
            technicians = [Technician(*row) for row in data]

            return technicians

    @classmethod
    def register_technician(cls, technician: Technician):
        with Database().connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO persons (first_name, last_name, phone_number, email, address, birth_date)
                VALUES(%s,%s,%s,%s,%s,%s)
                RETURNING ID
                """,
                (
                    technician.first_name,
                    technician.last_name,
                    technician.phone_number,
                    technician.email,
                    technician.address,
                    technician.birth_date,
                ),
            )
            person_id = cursor.fetchone()[0]

            cursor.execute(
                """
                INSERT INTO technicians (person_id)
                VALUES(%s)
                RETURNING ID
                """,
                (person_id,),
            )

            technician_id = cursor.fetchone()[0]

            return technician_id

    @classmethod
    def update_technician(cls, technician: Technician):
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
                    technician.first_name,
                    technician.last_name,
                    technician.phone_number,
                    technician.email,
                    technician.address,
                    technician.birth_date,
                    technician.id,
                ),
            )

            rows_count = cursor.rowcount

            return rows_count

    @classmethod
    def delete_technician(cls, technician: Technician):
        with Database().connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM PERSONS
                WHERE id = %s
                """,
                (technician.id,),
            )

            rows_count = cursor.rowcount
            return rows_count
