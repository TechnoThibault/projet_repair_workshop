from datetime import datetime

from models.technician import Technician


class RepairComment:
    def __init__(
        self,
        technician: Technician,
        comment: str,
        created_at: datetime,
        updated_at: datetime,
    ):
        self.technician = technician
        self.comment = comment
        self.created_at = created_at
        self.updated_at = updated_at

    @property
    def technician(self) -> Technician:
        return self.__technician

    @technician.setter
    def technician(self, technician: Technician):
        if not isinstance(technician, Technician):
            raise TypeError("Technician must be a Technician instance.")
        self.__technician = technician

    @property
    def comment(self) -> str:
        return self.__comment

    @comment.setter
    def comment(self, comment: str):
        if not isinstance(comment, str) or not comment.strip():
            raise ValueError("Comment must be a non-empty string.")
        self.__comment = comment.strip()

    @property
    def created_at(self) -> datetime:
        return self.__created_at

    @created_at.setter
    def created_at(self, created_at: datetime):
        if not isinstance(created_at, datetime):
            raise TypeError("Created at must be a datetime object.")

        if created_at > datetime.now(created_at.tzinfo):
            raise ValueError("Creation date cannot be in the future.")

        self.__created_at = created_at

    @property
    def updated_at(self) -> datetime:
        return self.__updated_at

    @updated_at.setter
    def updated_at(self, updated_at: datetime):
        if not isinstance(updated_at, datetime):
            raise TypeError("Updated at must be a datetime object.")

        if updated_at > datetime.now(updated_at.tzinfo):
            raise ValueError("Update date cannot be in the future.")

        if updated_at < self.__created_at:
            raise ValueError("Update date cannot be earlier than creation date.")

        self.__updated_at = updated_at
