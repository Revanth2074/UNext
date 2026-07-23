"""Models for representing ticket data."""

from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Ticket:
    """Represents a validated and processed support ticket.

    Attributes:
        ticket_id (str): Unique identifier of the ticket.
        customer_name (str): Name of the corporate customer.
        category (str): Ticket category (e.g. billing, technical).
        priority_raw (str): Raw priority string (e.g. low, medium, high, critical).
        priority_score (int): Score mapping (1 to 4) calculated based on priority_raw.
        created_at (datetime): Datetime when the ticket was created.
        sla_hours (int): Number of hours allowed by the SLA.
        status (str): Current status of the ticket (e.g. open, closed).
        sla_breached (bool): Whether the ticket has breached its SLA.
    """

    ticket_id: str
    customer_name: str
    category: str
    priority_raw: str
    priority_score: int
    created_at: datetime
    sla_hours: int
    status: str
    sla_breached: bool

    def to_dict(self) -> dict:
        """Convert the Ticket object to a dictionary serializable to JSON.

        Returns:
            dict: The dictionary representation of the ticket.
        """
        data = asdict(self)
        # Convert datetime to ISO format string
        data["created_at"] = self.created_at.isoformat()
        return data
