"""In-memory data store for managing tickets loaded from the JSON report."""

import json
import os
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from ticket_processor.config import PRIORITY_MAP, CLOSED_STATUSES, DATE_FORMAT

logger = logging.getLogger("ticket_api.store")


class TicketStore:
    """Manages an in-memory collection of tickets loaded from the JSON report."""

    def __init__(self) -> None:
        self.tickets: List[Dict[str, Any]] = []

    def load_from_file(self, file_path: str) -> None:
        """Loads tickets from the generated JSON report.

        Args:
            file_path (str): Path to the tickets_report.json file.
        """
        if not os.path.exists(file_path):
            logger.warning("Report file not found at %s. Initializing with empty list.", file_path)
            self.tickets = []
            return

        try:
            logger.info("Loading ticket data from report: %s", file_path)
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.tickets = data.get("tickets", [])
            logger.info("Successfully loaded %d tickets into memory.", len(self.tickets))
        except Exception as e:
            logger.error("Failed to load report file %s: %s", file_path, e)
            self.tickets = []

    def get_all(self, sort_by_priority: bool = True) -> List[Dict[str, Any]]:
        """Returns all tickets. Optionally sorted by priority score descending.

        Args:
            sort_by_priority (bool): If True, sorts tickets descending by priority score.

        Returns:
            List[Dict[str, Any]]: List of tickets.
        """
        # Recalculate SLA breach status dynamically to stay accurate to "now"
        now = datetime.now()
        for ticket in self.tickets:
            self._update_sla_breach_status(ticket, now)

        if sort_by_priority:
            # Sort by priority_score descending (stretch goal: Sort GET /tickets results by priority_score descending)
            return sorted(self.tickets, key=lambda t: t.get("priority_score", 0), reverse=True)
        return self.tickets

    def get_breached(self) -> List[Dict[str, Any]]:
        """Returns all tickets that have breached their SLA.

        Returns:
            List[Dict[str, Any]]: List of breached tickets.
        """
        now = datetime.now()
        breached_tickets = []
        for ticket in self.tickets:
            self._update_sla_breach_status(ticket, now)
            if ticket.get("sla_breached"):
                breached_tickets.append(ticket)
        return breached_tickets

    def get_by_id(self, ticket_id: str) -> Optional[Dict[str, Any]]:
        """Returns a ticket by its ID, or None if not found.

        Args:
            ticket_id (str): The ID of the ticket.

        Returns:
            Dict[str, Any] or None: The ticket dictionary or None.
        """
        now = datetime.now()
        for ticket in self.tickets:
            if ticket.get("ticket_id") == ticket_id:
                self._update_sla_breach_status(ticket, now)
                return ticket
        return None

    def get_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Returns tickets filtered by category (stretch goal).

        Args:
            category (str): The category name.

        Returns:
            List[Dict[str, Any]]: List of matching tickets.
        """
        now = datetime.now()
        category_tickets = []
        for ticket in self.tickets:
            if ticket.get("category", "").lower() == category.lower():
                self._update_sla_breach_status(ticket, now)
                category_tickets.append(ticket)
        return category_tickets

    def get_summary(self) -> Dict[str, Any]:
        """Returns a live summary breakdown of the current tickets in memory (stretch goal).

        Returns:
            Dict[str, Any]: Summary dictionary.
        """
        now = datetime.now()
        total = len(self.tickets)
        breached = 0
        by_category: Dict[str, int] = {}

        for ticket in self.tickets:
            self._update_sla_breach_status(ticket, now)
            if ticket.get("sla_breached"):
                breached += 1
            cat = ticket.get("category", "unknown")
            by_category[cat] = by_category.get(cat, 0) + 1

        return {
            "total_tickets": total,
            "breached_count": breached,
            "by_category": by_category,
        }

    def add(self, ticket_data: Dict[str, Any]) -> Dict[str, Any]:
        """Adds a new ticket to the store, calculating priority_score and sla_breached.

        Args:
            ticket_data (Dict[str, Any]): Dictionary of fields for the new ticket.

        Returns:
            Dict[str, Any]: The newly created ticket.
        """
        priority_raw = ticket_data["priority_raw"].lower()
        priority_score = PRIORITY_MAP.get(priority_raw, 1)

        # Convert created_at string (assumed format) to ISO string
        created_at_str = ticket_data["created_at"]
        try:
            dt = datetime.strptime(created_at_str, DATE_FORMAT)
            created_at_iso = dt.isoformat()
        except ValueError:
            # Fallback to current time if format is wrong, or assume it's already ISO
            try:
                dt = datetime.fromisoformat(created_at_str)
                created_at_iso = created_at_str
            except ValueError:
                dt = datetime.now()
                created_at_iso = dt.isoformat()

        # Calculate SLA breach
        status = ticket_data["status"].lower()
        sla_hours = ticket_data["sla_hours"]
        sla_deadline = dt + timedelta(hours=sla_hours)
        sla_breached = (sla_deadline < datetime.now()) and (status not in CLOSED_STATUSES)

        new_ticket = {
            "ticket_id": ticket_data["ticket_id"],
            "customer_name": ticket_data["customer_name"],
            "category": ticket_data["category"],
            "priority_raw": ticket_data["priority_raw"],
            "priority_score": priority_score,
            "created_at": created_at_iso,
            "sla_hours": sla_hours,
            "status": ticket_data["status"],
            "sla_breached": sla_breached,
        }

        self.tickets.append(new_ticket)
        return new_ticket

    def update(
        self, ticket_id: str, priority_raw: Optional[str] = None, status: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Updates an existing ticket's status and/or priority_raw.

        Args:
            ticket_id (str): The ID of the ticket to update.
            priority_raw (str or None): The new priority raw string.
            status (str or None): The new status string.

        Returns:
            Dict[str, Any] or None: The updated ticket or None if not found.
        """
        ticket = self.get_by_id(ticket_id)
        if not ticket:
            return None

        if priority_raw is not None:
            ticket["priority_raw"] = priority_raw
            ticket["priority_score"] = PRIORITY_MAP.get(priority_raw.lower(), 1)

        if status is not None:
            ticket["status"] = status

        # Recalculate breach status after status/priority changes
        self._update_sla_breach_status(ticket, datetime.now())
        return ticket

    def delete(self, ticket_id: str) -> bool:
        """Removes a ticket from the store.

        Args:
            ticket_id (str): ID of the ticket to delete.

        Returns:
            bool: True if deleted, False if not found.
        """
        for idx, ticket in enumerate(self.tickets):
            if ticket.get("ticket_id") == ticket_id:
                self.tickets.pop(idx)
                return True
        return False

    def _update_sla_breach_status(self, ticket: Dict[str, Any], now: datetime) -> None:
        """Updates the sla_breached status in-place for a ticket relative to 'now'."""
        status = ticket.get("status", "").lower()
        if status in CLOSED_STATUSES:
            ticket["sla_breached"] = False
            return

        created_at_str = ticket.get("created_at", "")
        sla_hours = ticket.get("sla_hours", 0)

        try:
            # Handle ISO format (2026-07-23T12:00:00) or CSV format (2026-07-23 12:00:00)
            if "T" in created_at_str:
                created_at = datetime.fromisoformat(created_at_str)
            else:
                created_at = datetime.strptime(created_at_str, DATE_FORMAT)

            sla_deadline = created_at + timedelta(hours=sla_hours)
            ticket["sla_breached"] = sla_deadline < now
        except Exception:
            # Fallback if unparseable
            ticket["sla_breached"] = False


# Global single instance of the store
store = TicketStore()
