from enum import Enum


class RepairStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    WAITING_FOR_PARTS = "waiting_for_parts"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
