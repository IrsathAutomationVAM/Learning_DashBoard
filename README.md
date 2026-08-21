#  Learning Dashboard

A comprehensive application built to track daily learning logs, productivity metrics, certification progress, and AI-powered insights.

##  Features

* **Interactive Application (`app.py`):** Main entry point featuring dynamic metric cards, charts, and module navigation.
* **AI Integration (`ai_coach.py` & `ai_helper.py`):** AI-driven coaching features to summarize productivity and assist with learning goals.
* **Certification & Learning Modules:** Dedicated managers (`certification_table.py`, `learning_table.py`) for tracking ongoing skills and credentials.
* **Review System (`review_generator.py` & `monthly_review.py`):** Automated weekly and monthly productivity analysis.
* **Data Management (`database.py`):** Robust database handling, queries, and configurations (`config.json`).
* **Validation Suite (`Validation/`):** Diagnostic scripts to check database health, AI responses, and schemas.

---

## 🛠️ Project Structure

```text
├── Validation/
│   ├── check_db.py         # Inspects daily log rows and database status
│   ├── check_ai.py         # Tests AI helper integration and responses
│   ├── check_review.py     # Generates weekly summary coach reviews
│   └── View_tables.py      # Debugs database schemas and configurations
├── .env.example            # Environment variable template
├── .gitignore              # Git ignore file
├── ai_coach.py             # AI coaching core logic
├── ai_helper.py            # AI utility helper functions
├── app.py                  # Main Streamlit application
├── certification_table.py  # Certification data handler
├── config.json             # Application configurations and SQL queries
├── database.py             # Database connection and setup
├── learning_table.py       # Learning log data handler
├── monthly_review.py       # Monthly review module
├── requirements.txt        # Python package dependencies
└── review_generator.py     # Review generation logic
