# GrowthMate 
[![GrowthMate CI](https://github.com/IrsathAutomationVAM/Learning_DashBoard/actions/workflows/growthmate-ci.yml/badge.svg)](https://github.com/IrsathAutomationVAM/Learning_DashBoard/actions/workflows/growthmate-ci.yml)
### AI-Powered Learning, Productivity & Career Growth Assistant

GrowthMate is a personal productivity, learning, certification, and career development platform built using Streamlit, SQLite, and AI-powered coaching through OpenRouter/NVIDIA Nemotron.

## Features

- Dashboard
- Daily Review
- Learning Tracker
- Certification Tracker
- Weekly Review
- Monthly Review
- AI Coach

## Project Structure

```text
Grow_mate/
├── app.py
├── Agents/
├── Assets/
├── Config/
├── Database/
├── Validation/
├── requirements.txt
└── .env
```

## Installation

```bash
git clone -b Develop_Frame https://github.com/IrsathAutomationVAM/Learning_DashBoard.git
cd Grow_mate
python -m venv .venv
```

### Activate Environment

Windows:

```bash
.venv\Scripts\activate
```

Linux/Mac:

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Environment Configuration

Create `.env`

```env
App_Name=GrowthMate
OPENROUTER_API_KEY=YOUR_API_KEY
OPENROUTER_URL=https://openrouter.ai/api/v1/chat/completions
OPENROUTER_AI_MODEL=nvidia/llama-3.1-nemotron-nano-8b-v1
```

## Run Application

```bash
streamlit run app.py
```

## Configuration Files

### Config/config.json
Contains navigation, SQL scripts, categories, statuses and application settings.

### Config/prompts.json
Contains AI prompts for:
- Weekly Review
- Monthly Review
- AI Coach
- Learning Analysis
- Certification Analysis

### Config/user_persona.json
Contains user profile information used by AI.

## Database

SQLite database:

```text
Database/logs.db
```

Tables include:
- daily_logs
- learning_tracker
- certifications

## Architecture

```text
Streamlit UI
     ↓
Business Logic
     ↓
Prompt Management
     ↓
OpenRouter AI
     ↓
SQLite Database
```

## Validation Utilities

- check_ai.py
- check_db.py
- check_review.py
- View_tables.py

## Troubleshooting

### OpenRouter Error
Verify:
- OPENROUTER_API_KEY
- OPENROUTER_URL
- OPENROUTER_AI_MODEL

### Database Error
Verify:

```text
Database/logs.db
```

exists.

## Security

Add to `.gitignore`:

```text
.env
.venv/
__pycache__/
```

## Future Enhancements

- Goal Tracker
- AI Interview Coach
- Resume Analyzer
- PDF Export
- Team Dashboard
- Cloud Database Support

## Author

**Irsath Ahamed**

Software Testing Engineer | AI Engineer

---

**GrowthMate - Track. Learn. Improve. Grow.**
