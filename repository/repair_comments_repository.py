from psycopg.rows import dict_row

from db.database import Database
from models import Repair, RepairComment, Technician


class RepairCommentsRepository:
    """
    Repository responsible for managing repair comments in the database.
    """

    @staticmethod
    def _map_row(row) -> RepairComment:
        """
        Maps a database row to a RepairComment instance.

        Args:
            row (dict): A dictionary containing the repair comment and
                associated technician information retrieved from the database.

        Returns:
            RepairComment: A RepairComment instance populated with the
                database values.
        """
        technician = None
        if row["t_id"] is not None:
            technician = Technician(
                id=row["t_id"],
                first_name=row["first_name"],
                last_name=row["last_name"],
                phone_number=row["phone_number"],
                email=row["email"],
                address=row["address"],
                birth_date=row["birth_date"],
            )

        repair_comment = RepairComment(
            id=row["rc_id"],
            comment=row["comment"],
            technician=technician,
            created_at=row["rc_created_at"],
            updated_at=row["rc_updated_at"],
        )
        return repair_comment

    @classmethod
    def get_repair_comments(cls, repair_id: int):
        """
        Retrieves all comments associated with a specific repair.

        Args:
            repair_id (int): The ID of the repair whose comments should
                be retrieved.

        Returns:
            list[RepairComment]: A list of RepairComment instances
                associated with the specified repair.
        """
        with Database().connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                SELECT 
                rc.id as rc_id,
                rc.comment,
                rc.created_at as rc_created_at,
                rc.updated_at as rc_updated_at,

                p.id as t_id,
                p.first_name,
                p.last_name,
                p.phone_number,
                p.email,
                p.address,
                p.birth_date
                from repair_comments rc
                left join technicians t on t.id = rc.technician_id
                left join persons p on p.id = t.person_id 
                where rc.repair_id = %s""",
                (repair_id,),
            )
            rows = cursor.fetchall()

            repair_comments = [RepairCommentsRepository._map_row(row) for row in rows]
            return repair_comments

    @classmethod
    def add_repair_comment(cls, repair_comment: RepairComment, repair: Repair):
        """
        Adds a new comment to a repair.

        Args:
            repair_comment (RepairComment): The comment instance containing
                the comment text and associated technician.
            repair (Repair): The repair instance to which the comment
                will be associated.

        Returns:
            int: The ID of the newly created repair comment.
        """
        with Database().connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO repair_comments (repair_id, technician_id, comment)
                VALUES
                (%s,%s,%s)
                returning ID;
                """,
                (repair.id, repair_comment.technician.id, repair_comment.comment),
            )
            repair_comment_id = cursor.fetchone()[0]
            return repair_comment_id
