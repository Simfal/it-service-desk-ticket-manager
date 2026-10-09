"""Automated tests for Service Desk business logic."""

from __future__ import annotations

import unittest
from datetime import datetime, timedelta

from src.models import Ticket
from src.service_desk import (
    build_report,
    calculate_priority,
    sla_status,
    summarise_tickets,
)


class PriorityTests(unittest.TestCase):
    def test_high_impact_high_urgency_is_p1(self) -> None:
        self.assertEqual(
            calculate_priority("high", "high"),
            "P1",
        )

    def test_medium_impact_high_urgency_is_p2(self) -> None:
        self.assertEqual(
            calculate_priority("medium", "high"),
            "P2",
        )

    def test_low_impact_low_urgency_is_p4(self) -> None:
        self.assertEqual(
            calculate_priority("low", "low"),
            "P4",
        )


class SLATests(unittest.TestCase):
    def make_ticket(
        self,
        *,
        impact: str = "high",
        urgency: str = "high",
        status: str = "open",
        opened_hours_ago: int = 1,
        resolved_after_hours: int | None = None,
    ) -> Ticket:
        now = datetime(2026, 10, 9, 12, 0)

        opened_at = now - timedelta(
            hours=opened_hours_ago
        )

        resolved_at = None

        if resolved_after_hours is not None:
            resolved_at = opened_at + timedelta(
                hours=resolved_after_hours
            )

        return Ticket(
            ticket_id="INC001",
            user="Test User",
            department="IT",
            category="Network",
            summary="Example issue",
            impact=impact,
            urgency=urgency,
            status=status,
            opened_at=opened_at,
            resolved_at=resolved_at,
        )

    def test_open_p1_ticket_on_track(self) -> None:
        now = datetime(2026, 10, 9, 12, 0)

        ticket = self.make_ticket(
            opened_hours_ago=1
        )

        self.assertEqual(
            sla_status(ticket, now),
            "ON TRACK",
        )

    def test_open_p1_ticket_at_risk(self) -> None:
        now = datetime(2026, 10, 9, 12, 0)

        ticket = self.make_ticket(
            opened_hours_ago=3
        )

        self.assertEqual(
            sla_status(ticket, now),
            "AT RISK",
        )

    def test_open_p1_ticket_breached(self) -> None:
        now = datetime(2026, 10, 9, 12, 0)

        ticket = self.make_ticket(
            opened_hours_ago=5
        )

        self.assertEqual(
            sla_status(ticket, now),
            "BREACHED",
        )

    def test_resolved_ticket_met_sla(self) -> None:
        ticket = self.make_ticket(
            status="resolved",
            resolved_after_hours=2,
        )

        self.assertEqual(
            sla_status(ticket),
            "MET",
        )

    def test_summary_counts_tickets(self) -> None:
        now = datetime(2026, 10, 9, 12, 0)

        tickets = [
            self.make_ticket(
                opened_hours_ago=1
            ),
            self.make_ticket(
                impact="low",
                urgency="low",
                status="resolved",
                opened_hours_ago=10,
                resolved_after_hours=2,
            ),
        ]

        summary = summarise_tickets(
            tickets,
            now=now,
        )

        self.assertEqual(
            summary["total"],
            2,
        )

        self.assertEqual(
            summary["open"],
            1,
        )

        self.assertEqual(
            summary["resolved"],
            1,
        )

    def test_report_lists_high_priority_open_tickets(
        self,
    ) -> None:
        now = datetime(2026, 10, 9, 12, 0)

        ticket = self.make_ticket(
            opened_hours_ago=1
        )

        report = build_report(
            [ticket],
            now=now,
        )

        self.assertIn(
            "High priority open tickets",
            report,
        )

        self.assertIn(
            "INC001 | P1 | Network | Example issue",
            report,
        )


if __name__ == "__main__":
    unittest.main()
