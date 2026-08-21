# Learning Dashboard

A comprehensive dashboard application built to track daily learning logs, productivity metrics, certification progress, and AI-powered reviews.

## Features

* **Interactive Dashboard:** High-level metric cards (`Daily Logs`, `Learnings`, `Certifications`, and `Avg Productivity`).
* **Visual Analytics:** Built-in line charts for productivity trends and bar charts for learning category distributions.
* **Certification Tracking:** Progress bars and dynamic tracking tables for ongoing and completed certifications.
* **Validation & Testing Tools:** Dedicated verification scripts to check database health, test AI helper responses, and generate weekly review insights.

---

## 🛠️ Project Structure

```text
├── Validation/
│   ├── check_db.py         # Inspects daily log rows and database status
│   ├── check_ai.py         # Tests AI helper integration and responses
│   ├── check_review.py     # Generates weekly summary coach reviews
│   └── View_tables.py      # Debugs database schemas and configurations
├── app.py                  # Main Streamlit/Python application
├── config.json             # App configurations and SQL query scripts
└── README.md
