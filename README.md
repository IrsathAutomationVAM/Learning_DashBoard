#  GrowthMate

GrowthMate is an AI-powered personal learning, productivity, and career growth assistant built using Python, Streamlit, SQLite, and OpenRouter.

The application helps users track daily accomplishments, learning activities, certification progress, generate performance reviews, and receive AI-powered coaching recommendations.

---

##  Features

###  Daily Review
- Track daily accomplishments
- Record learnings
- Capture blockers
- Plan next-day activities
- Track productivity score

###  Learning Tracker
- Log learning activities
- Categorize learnings
- Monitor continuous skill development

###  Weekly Review
- Generate AI-powered weekly summaries
- Highlight achievements
- Identify challenges and improvement opportunities

###  Monthly Review
- Generate professional self-review reports
- Useful for appraisals and one-on-one discussions

###  AI Coach
- Personalized learning recommendations
- Career development guidance
- Strength and skill-gap analysis
- Goal-oriented coaching insights

###  Certification Tracker
- Track certification progress
- Monitor completion status
- Maintain certification roadmap

###  Dashboard
- Daily activity metrics
- Learning analytics
- Certification progress visualization
- Productivity trends

###  History Viewer
- Review historical activity records
- Track personal growth over time

---

##  Technology Stack

### Frontend
- Streamlit

### Backend
- Python

### Database
- SQLite

### AI Integration
- OpenRouter
- Large Language Models (LLMs)

### Libraries
- Pandas
- Requests
- Python Dotenv

---

## 📂 Project Structure

```text
Grow_mate/

├── app.py
├── ai_helper.py
├── ai_coach.py
├── review_generator.py
├── monthly_review.py
├── database.py
├── config.json
├── requirements.txt
├── logs.db
│
├── Validation/
│   ├── check_ai.py
│   ├── check_db.py
│   ├── check_review.py
│   └── View_tables.py
│
└── .env
```
---------
###⚙️ Installation
#Clone Repository
```
git clone https://github.com/IrsathAutomationVAM/Learning_DashBoard/GrowthMate.git
cd GrowthMate
```
--------
### Create Virtual Environmental
```
python -m venv .venv
```
### Activate Virtual Environment

#Windows:
```
.venv\Scripts\activate
```

###Install Dependencies
```
pip install -r requirements.txt
```

###Environment Variables

#Create a .env file:
```
OPENROUTER_API_KEY=your_api_key

OPENROUTER_URL=https://openrouter.ai/api/v1/chat/completions

OPENROUTER_AI_MODEL=openai/gpt-4o-mini

App_Name=GrowthMate
```

###Run Application
```
streamlit run app.py
```

### Application Launch on:
```
http://localhost:8501
```
