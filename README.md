
Python IT Service Desk project that prioritises incidents, monitors SLA status, validates ticket data and produces support reports.
# IT Service Desk Ticket Manager

A beginner Python project that simulates part of a real IT Service Desk workflow.

The application reads IT support tickets from CSV, validates the data, calculates ticket priority, identifies SLA risk, produces summary statistics, and exports a management report.

## Why I built this

I built this project to strengthen my practical IT support and Python skills while learning how common Service Desk concepts such as incident priority, SLA tracking, ticket categorisation, escalation, and reporting can be represented in software.

## Features

- Import support tickets from CSV
- Validate ticket fields
- Calculate priority from impact and urgency
- Track SLA targets
- Flag tickets that are approaching or have breached SLA
- Summarise tickets by status, category and priority
- Export a clear text report
- Log application activity and validation errors
- Command-line interface
- Automated unit tests using Python's built-in `unittest`
- No third-party Python packages required

## Example ticket categories

- Account Access
- Hardware
- Software
- Network
- Email
- Security

## Project structure

```text
it-service-desk-ticket-manager/
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── data/
│   └── tickets.csv
├── docs/
│   └── interview-notes.md
├── reports/
│   └── sample_report.txt
├── src/
│   ├── __init__.py
│   ├── models.py
│   ├── service_desk.py
│   └── main.py
└── tests/
    └── test_service_desk.py
```

## Priority matrix

Priority is calculated from **impact** and **urgency**.

| Impact | Urgency | Priority |
|---|---|---|
| High | High | P1 |
| High | Medium | P2 |
| Medium | High | P2 |
| High | Low | P3 |
| Medium | Medium | P3 |
| Low | High | P3 |
| Medium | Low | P4 |
| Low | Medium | P4 |
| Low | Low | P4 |

## SLA targets

| Priority | Target resolution time |
|---|---:|
| P1 | 4 hours |
| P2 | 8 hours |
| P3 | 24 hours |
| P4 | 72 hours |

For demonstration purposes, unresolved tickets are marked:

- `BREACHED` when the ticket age is greater than the SLA target
- `AT RISK` when at least 75% of the SLA target has elapsed
- `ON TRACK` otherwise

## How to run



Clone the repository and move into the project directory:

```bash
git clone https://github.com/YOUR-USERNAME/it-service-desk-ticket-manager.git
cd it-service-desk-ticket-manager
```

Run the application:

```bash
python -m src.main
```

You can specify a different input file and report location:

```bash
python -m src.main --input data/tickets.csv --output reports/report.txt
```

Run the automated tests:

```bash
python -m unittest discover -s tests -v
```

## Example output

```text
IT SERVICE DESK REPORT
======================
Total tickets: 12
Open tickets: 8
Resolved tickets: 4
SLA breached: 2
SLA at risk: 2

Tickets by priority
-------------------
P1: 2
P2: 3
P3: 4
P4: 3
```

## Skills demonstrated

This project demonstrates:

- Python fundamentals
- Object-oriented programming
- CSV processing
- Data validation
- Exception handling
- Logging
- Functions and modules
- Dictionaries and collections
- Date/time calculations
- Command-line arguments
- Automated testing
- ITIL-style incident prioritisation concepts
- SLA monitoring
- Service Desk reporting
- Git/GitHub project structure

## Possible future improvements

- Add a SQLite database
- Build a graphical interface
- Add ticket assignment and technician workload balancing
- Add authentication and role-based access
- Export reports to CSV or Excel
- Create a web dashboard
- Add email notifications for breached SLA tickets
- Integrate with Microsoft Entra ID or Microsoft Graph in a future version

