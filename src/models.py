"""Domain models used by the Service Desk application."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


VALID_LEVELS = {"low", "medium", "high"}
VALID_STATUSES = {"open", "in progress", "resolved", "closed"}


@dataclass
class Ticket:
    """Represents a single IT support ticket."""

    ticket_id: str
    user: str
    department: str
    category: str
    summary: str
    impact: str
    urgency: str
    status: str
    opened_at: datetime
    resolved_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        self.impact = self.impact.strip().lower()
        self.urgency = self.urgency.strip().lower()
        self.status = self.status.strip().lower()

        if not self.ticket_id.strip():
            raise ValueError("ticket_id cannot be empty")
        if not self.user.strip():
            raise ValueError(f"{self.ticket_id}: user cannot be empty")
        if self.impact not in VALID_LEVELS:
            raise ValueError(
                f"{self.ticket_id}: invalid impact '{self.impact}'. "
                f"Expected one of {sorted(VALID_LEVELS)}"
            )
        if self.urgency not in VALID_LEVELS:
            raise ValueError(
                f"{self.ticket_id}: invalid urgency '{self.urgency}'. "
                f"Expected one of {sorted(VALID_LEVELS)}"
            )
        if self.status not in VALID_STATUSES:
            raise ValueError(
                f"{self.ticket_id}: invalid status '{self.status}'. "
                f"Expected one of {sorted(VALID_STATUSES)}"
            )
        if self.resolved_at and self.resolved_at < self.opened_at:
            raise ValueError(
                f"{self.ticket_id}: resolved_at cannot be earlier than opened_at"
            )

    @property
    def is_resolved(self) -> bool:
        """Return True when the ticket is resolved or closed."""
        return self.status in {"resolved", "closed"}
