from psycopg.rows import dict_row

from db.database import Database
from models import Part, Repair, RepairPart


class RepairPartsRepository:
    """
    Repository responsible for managing parts associated with repairs
    in the database.
    """

    @staticmethod
    def _map_row(row) -> RepairPart:
        """
        Maps a database row to a RepairPart instance.

        Args:
            row (dict): A dictionary containing repair part and
                associated part information retrieved from the database.

        Returns:
            RepairPart: A RepairPart instance populated with the
                database values.
        """
        part = None
        if row["p_id"] is not None:
            part = Part(
                id=row["p_id"],
                name=row["p_name"],
                description=row["p_description"],
                unit_price=float(row["p_unit_price"]),
                stock_quantity=int(row["p_stock_quantity"]),
                created_at=row["p_created_at"],
                updated_at=row["p_updated_at"],
            )

        repair_part = RepairPart(
            id=row["rp_id"],
            part=part,
            quantity=int(row["rp_quantity"]),
            unit_price=float(row["rp_unit_price"]),
        )
        return repair_part

    @classmethod
    def get_repair_parts(cls, repair_id: int):
        """
        Retrieves all parts associated with a specific repair.

        Args:
            repair_id (int): The ID of the repair whose parts should
                be retrieved.

        Returns:
            list[RepairPart]: A list of RepairPart instances associated
                with the specified repair.
        """
        with Database().connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                SELECT 
                rp.id as rp_id,
                rp.quantity as rp_quantity,
                rp.unit_price as rp_unit_price,

                p.id as p_id,
                p.name as p_name,
                p.description as p_description,
                p.unit_price as p_unit_price,
                p.stock_quantity as p_stock_quantity,
                p.created_at as p_created_at,
                p.updated_at as p_updated_at

                from repair_parts rp
                left join parts p on p.id = rp.part_id 
                where rp.repair_id = %s""",
                (repair_id,),
            )
            rows = cursor.fetchall()

            repair_parts = [RepairPartsRepository._map_row(row) for row in rows]
            return repair_parts

    @classmethod
    def add_repair_part(cls, repair_part: RepairPart, repair: Repair):
        """
        Adds a part to a repair.

        Args:
            repair_part (RepairPart): The repair part instance containing
                the associated part, quantity, and unit price.
            repair (Repair): The repair instance to which the part
                will be associated.

        Returns:
            RepairPart: The updated RepairPart instance, including
                its newly assigned database ID.
        """
        with Database().connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO repair_parts (
                    repair_id,
                    part_id,
                    quantity,
                    unit_price
                )
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """,
                (
                    repair.id,
                    repair_part.part.id,
                    repair_part.quantity,
                    repair_part.unit_price,
                ),
            )

            repair_part.id = cursor.fetchone()[0]

        return repair_part
