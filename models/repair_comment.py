from datetime import datetime

from models.technician import Technician


class RepairComment:
    def __init__(
        self,
        id: int,
        comment: str,
        technician: Technician | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        self.id = id
        self.technician = technician
        self.comment = comment
        if created_at is None:
            created_at = datetime.now()
        self.created_at = created_at
        if updated_at is None:
            updated_at = datetime.now()
        self.updated_at = updated_at

    def __str__(self) -> str:
        technician = str(self.technician) if self.technician else "Unassigned"

        return (
            f"\n    ┌── Comment #{self.id}"
            f"\n    │"
            f"\n    │   {self.comment}"
            f"\n    │"
            f"\n    ├── Technician: {technician}"
            f"\n    ├── Created: {self.created_at:%Y-%m-%d %H:%M}"
            f"\n    └── Updated: {self.updated_at:%Y-%m-%d %H:%M}"
        )

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, id: int):
        if not isinstance(id, int):
            raise TypeError("The ID must be a integer.")
        self.__id = id

    @property
    def technician(self) -> Technician:
        return self.__technician

    @technician.setter
    def technician(self, technician: Technician):
        if technician and not isinstance(technician, Technician):
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

    @classmethod
    def validate_comment(cls, value):
        if not value.strip():
            raise ValueError("The comment cannot be empty.")
