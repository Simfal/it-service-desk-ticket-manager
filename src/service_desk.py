"""Core Service Desk logic for ticket loading, prioritisation and reporting."""

from __future__ import annotations

import csv
import logging
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Iterable

from .models import Ticket


LOGGER = logging.getLogger(__name__)

PRIORITY_MATRIX = {
    ("high", "high"): "P1",
    ("high", "medium"): "P2",
    ("medium", "high"): "P2",
    ("high", "low"): "P3",
    ("medium", "medium"): "P3",
    ("low", "high"): "P3",
    ("medium", "low"): "P4",
    ("low", "medium"): "P4",
    ("low", "low"): "P4",
}

SLA_HOURS = {
    "P1": 4,
    "P2": 8,
    "P3": 24,
    "P4": 72,
}

DATE_FORMAT = "%Y-%m-%d %H:%M"


def parse_datetime(value: str) -> datetime | None:
    """Parse a CSV datetime value. Empty strings become None."""
    value = value.strip()
    if not value:
        return None
    return datetime.strptime(value, DATE_FORMAT)


def calculate_priority(impact: str, urgency: str) -> str:
    """Return P1-P4 using the configured impact/urgency matrix."""
    key = (impact.strip().lower(), urgency.strip().lower())
    try:
        return PRIORITY_MATRIX[key]
    except KeyError as exc:
        raise ValueError(f"Invalid impact/urgency combination: {key}") from exc


def sla_status(ticket: Ticket, now: datetime | None = None) -> str:
    """Return ON TRACK, AT RISK, BREACHED or MET for a ticket."""
    priority = calculate_priority(ticket.impact, ticket.urgency)
    target_hours = SLA_HOURS[priority]

    end_time = ticket.resolved_at if ticket.resolved_at else (now or datetime.now())
    age_hours = (end_time - ticket.opened_at).total_seconds() / 3600

    if ticket.is_resolved:
        return "MET" if age_hours <= target_hours else "BREACHED"
    if age_hours > target_hours:
        return "BREACHED"
    if age_hours >= target_hours * 0.75:
        return "AT RISK"
    return "ON TRACK"


def load_tickets(path: str | Path) -> list[Ticket]:
    """Load and validate tickets from a CSV file."""
    csv_path = Path(path)
    tickets: list[Ticket] = []

    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {
            "ticket_id",
            "user",
            "department",
            "category",
            "summary",
            "impact",
            "urgency",
            "status",
            "opened_at",
            "resolved_at",
        }

        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"CSV is missing required columns: {sorted(missing)}")

        for row_number, row in enumerate(reader, start=2):
            try:
                opened_at = parse_datetime(row["opened_at"])
                if opened_at is None:
                    raise ValueError("opened_at cannot be empty")

                ticket = Ticket(
                    ticket_id=row["ticket_id"].strip(),
                    user=row["user"].strip(),
                    department=row["department"].strip(),
                    category=row["category"].strip(),
                    summary=row["summary"].strip(),
                    impact=row["impact"],
                    urgency=row["urgency"],
                    status=row["status"],
                    opened_at=opened_at,
                    resolved_at=parse_datetime(row["resolved_at"]),
                )
                tickets.append(ticket)
            except (ValueError, KeyError) as exc:
                LOGGER.error("Skipping invalid row %s: %s", row_number, exc)

    LOGGER.info("Loaded %s valid tickets from %s", len(tickets), csv_path)
    return tickets


def summarise_tickets(
    tickets: Iterable[Ticket], now: datetime | None = None
) -> dict[str, object]:
    """Produce summary statistics for a collection of tickets."""
    ticket_list = list(tickets)
    priorities = Counter(
        calculate_priority(ticket.impact, ticket.urgency) for ticket in ticket_list
    )
    statuses = Counter(ticket.status for ticket in ticket_list)
    categories = Counter(ticket.category for ticket in ticket_list)
    sla_states = Counter(sla_status(ticket, now=now) for ticket in ticket_list)

    return {
        "total": len(ticket_list),
        "open": sum(1 for ticket in ticket_list if not ticket.is_resolved),
        "resolved": sum(1 for ticket in ticket_list if ticket.is_resolved),
        "priorities": priorities,
        "statuses": statuses,
        "categories": categories,
        "sla_states": sla_states,
    }


def build_report(tickets: Iterable[Ticket], now: datetime | None = None) -> str:
    """Build a human-readable Service Desk report."""
    ticket_list = list(tickets)
    summary = summarise_tickets(ticket_list, now=now)

    lines = [
        "IT SERVICE DESK REPORT",
        "======================",
        f"Total tickets: {summary['total']}",
        f"Open tickets: {summary['open']}",
        f"Resolved tickets: {summary['resolved']}",
        f"SLA breached: {summary['sla_states'].get('BREACHED', 0)}",
        f"SLA at risk: {summary['sla_states'].get('AT RISK', 0)}",
        "",
        "Tickets by priority",
        "-------------------",
    ]

    for priority in ("P1", "P2", "P3", "P4"):
        lines.append(f"{priority}: {summary['priorities'].get(priority, 0)}")

    lines.extend(["", "Tickets by category", "-------------------"])
    for category, count in sorted(summary["categories"].items()):
        lines.append(f"{category}: {count}")

    lines.extend(["", "Ticket details", "--------------"])
    for ticket in sorted(ticket_list, key=lambda item: item.ticket_id):
        priority = calculate_priority(ticket.impact, ticket.urgency)
        lines.append(
            f"{ticket.ticket_id} | {priority} | {sla_status(ticket, now=now)} | "
            f"{ticket.status.title()} | {ticket.category} | {ticket.summary}"
        )

    return "\n".join(lines) + "\n"


def save_report(report: str, output_path: str | Path) -> None:
    """Save a report to disk, creating the parent folder if required."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report, encoding="utf-8")
    LOGGER.info("Report saved to %s", path)
