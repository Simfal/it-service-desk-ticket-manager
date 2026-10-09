"""Command-line entry point for the IT Service Desk Ticket Manager."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from .service_desk import build_report, load_tickets, save_report


def configure_logging() -> None:
    """Configure console and file logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler("service_desk.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyse IT support tickets and generate an SLA report."
    )
    parser.add_argument(
        "--input",
        default="data/tickets.csv",
        help="Path to the input CSV file (default: data/tickets.csv)",
    )
    parser.add_argument(
        "--output",
        default="reports/report.txt",
        help="Path to the output report (default: reports/report.txt)",
    )
    return parser.parse_args()


def main() -> int:
    configure_logging()
    args = parse_args()

    try:
        tickets = load_tickets(Path(args.input))
        report = build_report(tickets)
        save_report(report, Path(args.output))
        print(report)
        return 0
    except (FileNotFoundError, ValueError) as exc:
        logging.getLogger(__name__).error("Application error: %s", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
