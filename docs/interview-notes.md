# Interview Notes

## 30-second explanation

I created a Python Service Desk Ticket Manager that simulates a small part of an IT support workflow. It reads ticket data from CSV, validates each incident, calculates priority using impact and urgency, checks SLA status, produces management statistics, saves a report and records application activity in a log. I also wrote unit tests for the key business rules.

## Why this is relevant to IT support

The project helped me connect programming with real Service Desk concepts rather than building a purely academic application. I used common support ideas such as incidents, categories, impact, urgency, priority, escalation risk and SLA targets.

## Technical decisions

### Why CSV?
CSV keeps the first version simple and makes the underlying data easy to inspect. In a future version I would move the tickets into SQLite or another database.

### Why separate modules?
I separated the data model, business logic and command-line interface so the application is easier to understand, test and extend.

### Why automated tests?
The most important business rules are the priority matrix and SLA calculations. Tests help prove that changes to the application do not accidentally break those rules.

### What I would improve next

1. Store tickets in SQLite.
2. Add technician assignment.
3. Add a simple web interface.
4. Add authentication and role-based access control.
5. Export metrics to a dashboard.
6. Add simulated Active Directory account-management tickets.
