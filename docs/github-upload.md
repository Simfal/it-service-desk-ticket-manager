# Uploading this project to GitHub

## 1. Create the repository

On GitHub, create a new public repository named:

`it-service-desk-ticket-manager`

Do not add another README, .gitignore, or licence when creating the repository because this project already includes them.

## 2. Open a terminal in the project folder

On Windows, open the extracted project folder, right-click an empty area and choose **Open in Terminal**.

## 3. Initialise Git

```bash
git init
git add .
git commit -m "Initial commit: IT Service Desk Ticket Manager"
git branch -M main
```

## 4. Connect it to GitHub

Replace the URL if your GitHub username differs:

```bash
git remote add origin https://github.com/Simfal/it-service-desk-ticket-manager.git
git push -u origin main
```

## 5. Suggested repository description

> Python IT Service Desk project that prioritises incidents, monitors SLA status, validates ticket data and produces support reports.

## 6. Suggested GitHub topics

Add these topics on the repository page:

`python` `it-support` `service-desk` `helpdesk` `itil` `sla` `cybersecurity` `portfolio-project`

## 7. Before sharing it with employers

Run:

```bash
python -m unittest discover -s tests -v
python -m src.main
```

Read `docs/interview-notes.md` and make sure you can explain the priority matrix, SLA logic, modules, and tests in your own words.
