from psycopg.rows import dict_row

from db.database import Database
from models import Customer, Device, Repair, RepairStatus, Technician


class RepairsRepository:
    """
    Repository to access the database about the Repairs.
    """

    @staticmethod
    def _map_row(row) -> Repair:
        """
        Tool to construct a Repair object based on data from the database.
        """

        customer = Customer(
            id=row["customer_id"],
            first_name=row["customer_first_name"],
            last_name=row["customer_last_name"],
            phone_number=row["customer_phone_number"],
            email=row["customer_email"],
            address=row["customer_address"],
            birth_date=row["customer_birth_date"],
            created_at=row["customer_created_at"],
        )

        device = Device(
            id=row["device_id"],
            customer=customer,
            brand=row["brand"],
            model=row["model"],
            serial_number=row["serial_number"],
            device_type=row["device_type"],
            created_at=row["device_created_at"],
        )

        technician = None

        if row["technician_id"] is not None:
            technician = Technician(
                id=row["customer_id"],
                first_name=row["customer_first_name"],
                last_name=row["customer_last_name"],
                phone_number=row["customer_phone_number"],
                email=row["customer_email"],
                address=row["customer_address"],
                birth_date=row["customer_birth_date"],
                created_at=row["customer_created_at"],
            )

        return Repair(
            id=row["repair_id"],
            device=device,
            description=row["description"],
            status=RepairStatus(row["status"]),
            labor_cost=float(row["labor_cost"]),
            technician=technician,
            created_at=row["repair_created_at"],
            updated_at=row["repair_updated_at"],
        )

    @classmethod
    def get_repairs(cls, status: RepairStatus | None = None):
        with Database().connection.cursor(row_factory=dict_row) as cursor:

            query = """
                    SELECT
                        r.id AS repair_id,
                        r.description,
                        r.status,
                        r.labor_cost,
                        r.created_at AS repair_created_at,
                        r.updated_at AS repair_updated_at,

                        d.id AS device_id,
                        d.brand,
                        d.model,
                        d.serial_number,
                        d.device_type,
                        d.created_at AS device_created_at,

                        pc.id AS customer_id,
                        pc.first_name AS customer_first_name,
                        pc.last_name AS customer_last_name,
                        pc.phone_number AS customer_phone_number,
                        pc.email AS customer_email,
                        pc.address AS customer_address,
                        pc.birth_date AS customer_birth_date,
                        pc.created_at AS customer_created_at,

                        pt.id AS technician_id,
                        pt.first_name AS technician_first_name,
                        pt.last_name AS technician_last_name,
                        pt.phone_number AS technician_phone_number,
                        pt.email AS technician_email,
                        pt.address AS technician_address,
                        pt.birth_date AS technician_birth_date,
                        pt.created_at AS technician_created_at

                    FROM repairs r
                    JOIN devices d ON r.device_id = d.id
                    JOIN customers c on d.customer_id = c.id
                    JOIN persons pc on c.person_id = pc.id
                    LEFT JOIN technicians t ON r.technician_id = t.id
                    LEFT JOIN persons pt ON t.person_id = pt.id
                """

            params = ()

            if status is not None:
                query += " WHERE r.status = %s "
                params = (status,)

            query += "ORDER BY r.id"

            cursor.execute(query, params)

            rows = cursor.fetchall()

            repairs = [RepairsRepository._map_row(row) for row in rows]

            return repairs
