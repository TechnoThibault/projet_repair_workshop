from db.database import Database
from models import Device


class DevicesRepository:
    """
    Repository responsible for managing device records in the database.
    """

    @classmethod
    def register_device(cls, device: Device):
        """
        Registers a new device in the database.

        Args:
            device (Device): The device instance containing the customer ID,
                brand, model, serial number, and device type.

        Returns:
            int: The ID of the newly registered device.
        """
        with Database().connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO devices (customer_id, brand, model, serial_number, device_type)
                VALUES (%s,%s,%s,%s,%s)
                RETURNING ID
                """,
                (
                    device.customer.id,
                    device.brand,
                    device.model,
                    device.serial_number,
                    device.device_type,
                ),
            )
            device_id = cursor.fetchone()[0]

            return device_id
