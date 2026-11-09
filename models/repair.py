from datetime import datetime

from helpers import Helpers
from models.device import Device
from models.enums import RepairStatus
from models.repair_comment import RepairComment
from models.repair_part import RepairPart
from models.technician import Technician


class Repair:
    def __init__(
        self,
        id: int,
        device: Device,
        description: str,
        status: RepairStatus,
        labor_cost: float,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        technician: Technician | None = None,
        parts: list[RepairPart] | None = None,
        comments: list[RepairComment] | None = None,
    ):
        self.id = id
        self.device = device
        self.technician = technician
        self.description = description
        self.status = status
        self.labor_cost = labor_cost
        if created_at is None:
            created_at = datetime.now()
        if updated_at is None:
            updated_at = datetime.now()
        self.created_at = created_at
        self.updated_at = updated_at

        self.__parts: list[RepairPart] = []
        self.__comments: list[RepairComment] = []

        if parts is not None:
            if not isinstance(parts, list):
                raise TypeError("Parts must be a list.")
            for part in parts:
                if not isinstance(part, RepairPart):
                    raise TypeError("Every item in parts must be a RepairPart.")
            self.__parts = parts.copy()

        if comments is not None:
            if not isinstance(comments, list):
                raise TypeError("Comments must be a list.")
            for comment in comments:
                if not isinstance(comment, RepairComment):
                    raise TypeError("Every item in comments must be a RepairComment.")
            self.__comments = comments.copy()

    def __str__(self) -> str:
        technician = str(self.technician) if self.technician else "Unassigned"

        header = (
            f"========================================"
            f"   REPAIR #{self.id}   "
            f"========================================"
        )

        separator = "=" * len(header)

        return (
            f"\n\n{header}"
            f"\n\n{self.description}"
            f"\n\n"
            f"Status: {self.status.name.replace('_', ' ').title()} | "
            f"Labor: €{self.labor_cost:.2f} | "
            f"Parts: €{self.total_parts_cost:.2f}"
            f"\nTotal: €{self.total_cost:.2f}"
            f"\nCreated: {Helpers.format_datetime(self.created_at)} | "
            f"Updated: {Helpers.format_datetime(self.updated_at)}"
            f"\n"
            f"│"
            f"\n├── Technician: {technician}"
            f"\n│"
            f"\n├── Device:"
            f"\n│   {self.device}"
            f"\n│"
            f"\n├── Parts ({len(self.parts)}):"
            f"{''.join(str(part) for part in self.parts) if self.parts else chr(10) + '    └── No parts assigned.'}"
            f"\n│"
            f"\n└── Comments ({len(self.comments)}):"
            f"{''.join(str(comment) for comment in self.comments) if self.comments else chr(10) + '    └── No comments.'}"
            f"\n{separator}"
        )

    @property
    def total_parts_cost(self):
        return sum(part.quantity * part.unit_price for part in self.parts)

    @property
    def total_cost(self):
        return self.labor_cost + self.total_parts_cost

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, id: int):
        if not isinstance(id, int):
            raise TypeError("The ID must be a integer.")
        self.__id = id

    @property
    def device(self) -> Device:
        return self.__device

    @device.setter
    def device(self, device: Device):
        if not isinstance(device, Device):
            raise TypeError("Device must be a Device instance.")
        self.__device = device

    @property
    def technician(self) -> Technician:
        return self.__technician

    @technician.setter
    def technician(self, technician: Technician):
        if technician and not isinstance(technician, Technician):
            raise TypeError("Technician must be a Technician instance.")
        self.__technician = technician

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, description: str):
        if not isinstance(description, str) or not description.strip():
            raise ValueError("Description must be a non-empty string.")
        self.__description = description.strip()

    @property
    def status(self) -> RepairStatus:
        return self.__status

    @status.setter
    def status(self, status: RepairStatus):
        self.__status = status

    @property
    def labor_cost(self) -> float:
        return self.__labor_cost

    @labor_cost.setter
    def labor_cost(self, labor_cost: float):
        if isinstance(labor_cost, bool) or not isinstance(labor_cost, (int, float)):
            raise TypeError("Labor cost must be a number.")

        if labor_cost < 0:
            raise ValueError("Labor cost cannot be negative.")

        self.__labor_cost = float(labor_cost)

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

    @property
    def parts(self) -> list[RepairPart]:
        return self.__parts.copy()

    @property
    def comments(self) -> list[RepairComment]:
        return self.__comments.copy()

    def add_part(self, part: RepairPart):
        if not isinstance(part, RepairPart):
            raise TypeError("Part must be a RepairPart instance.")
        self.__parts.append(part)

    def remove_part(self, part: RepairPart):
        if not isinstance(part, RepairPart):
            raise TypeError("Part must be a RepairPart instance.")
        self.__parts.remove(part)

    def add_comment(self, comment: RepairComment):
        if not isinstance(comment, RepairComment):
            raise TypeError("Comment must be a RepairComment instance.")
        self.__comments.append(comment)

    def remove_comment(self, comment: RepairComment):
        if not isinstance(comment, RepairComment):
            raise TypeError("Comment must be a RepairComment instance.")
        self.__comments.remove(comment)

    @classmethod
    def validate_description(cls, value):
        if not value.strip():
            raise ValueError("Description cannot be empty.")

    @classmethod
    def validate_status(cls, value):
        if value not in [status.value for status in RepairStatus]:
            raise ValueError("The status is not correct.")

    @classmethod
    def valid_labor_cost(cls, value):
        try:
            value = float(value)
            if value < 0:
                raise ValueError("Labor cost must be equal or greater than zero.")
        except ValueError:
            raise ValueError("Labor cost must be a number.")
