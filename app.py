# app.py

import json
import logging as log
import os
import sqlite3 as DB

import pandas as pd
import streamlit as st

from datetime import date
from dotenv import load_dotenv

from ai_helper import ask_ai
from ai_coach import get_ai_coaching
from review_generator import get_weekly_summary
from monthly_review import generate_monthly_review

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------

load_dotenv()

log.basicConfig(
    level=log.INFO,
    format="%(asctime)s - [%(filename)s:%(lineno)d] - %(levelname)s - %(message)s",
    handlers=[log.StreamHandler()],
    force=True
)
st.markdown("""
<style>

/* Main App Background */
.stApp {
    background-color: #0f172a;
}

/* Headers */
h1, h2, h3 {
    color: #f8fafc !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #1e293b;
    border-right: 1px solid #334155;
}

/* Text */
p, label, div {
    color: #e2e8f0;
}

/* Buttons */
.stButton button {
    background-color: #3b82f6;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 0.6rem 1rem;
    font-weight: 600;
}

.stButton button:hover {
    background-color: #2563eb;
}

/* Input Fields */
.stTextInput input,
.stTextArea textarea {
    background-color: #1e293b;
    color: white;
    border-radius: 8px;
}

/* Selectbox */
.stSelectbox div {
    border-radius: 8px;
}

/* Success Messages */
.stSuccess {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

with open("config.json", "r") as file:
    config_file = json.load(file)

# ---------------------------------------------------
# HELPERS
# ---------------------------------------------------

def get_connection():
    return DB.connect("logs.db")

# ---------------------------------------------------
# STREAMLIT CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title=os.getenv("App_Name", "GrowthMate"),
    layout="wide")

if "app_started" not in st.session_state:
    log.info("Application Launched Successfully")
    st.session_state.app_started = True

st.title(os.getenv("App_Name", "GrowthMate"))

page = st.sidebar.selectbox(
    "Select Module",
    config_file["Learning_Category"])

# ---------------------------------------------------
# DAILY REVIEW
# ---------------------------------------------------

if page == "Daily Review":

    st.header("Daily Review")

    accomplishments = st.text_area("What did you accomplish today?")

    learnings = st.text_area("What did you learn today?")

    blockers = st.text_area("Any blockers?")

    plan = st.text_area("Tomorrow's Plan")

    productivity = st.slider("Productivity Score",1,10,1)

    if st.button("Save Daily Review"):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            config_file["Save_Daily_review_Script"],
            (
                str(date.today()),
                accomplishments,
                learnings,
                blockers,
                plan,
                productivity
            )
        )

        conn.commit()
        conn.close()

        st.success("Daily Review Saved Successfully")

        log.info("Daily Review Saved")

# ---------------------------------------------------
# LEARNING TRACKER
# ---------------------------------------------------

elif page == "Learning Tracker":

    st.header(" Learning Tracker")

    learning_date = st.date_input("Learning Date")

    category = st.selectbox("Category",config_file["Learning_Concepts_Items"])

    learning = st.text_area("What did you learn today?")

    if st.button("Save Learning"):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            config_file["Insert_Learning_tracker_Script"],
            (
                str(learning_date),
                category,
                learning
            )
        )

        conn.commit()
        conn.close()

        st.success("Learning Saved Successfully")

        log.info("Learning Saved")

# ---------------------------------------------------
# WEEKLY REVIEW
# ---------------------------------------------------

elif page == "Weekly Review":

    st.header(" Weekly Review")

    if st.button("Generate Weekly Review"):

        weekly_data = get_weekly_summary()

        prompt = f"""
                    You are my personal career coach.
                    Analyze:

                    {weekly_data}

                    Provide:

                    1. Key Achievements
                    2. Learning Summary
                    3. Challenges
                    4. Areas For Improvement
                    5. Recommendations
                    6. Next Week Goals
                    """

        review = ask_ai(prompt)
        st.write(review)
        log.info("Weekly Review Generated")

# ---------------------------------------------------
# VIEW HISTORY
# ---------------------------------------------------

elif page == "View History":

    st.header(" View History")

    conn = get_connection()

    data = pd.read_sql_query(config_file["View_History_Script"], conn)

    conn.close()

    st.dataframe(data)

    log.info("History Loaded")

# ---------------------------------------------------
# CERTIFICATION TRACKER
# ---------------------------------------------------

elif page == "Certification Tracker":

    st.header(" Certification Tracker")

    cert_name = st.text_input("Certification Name")

    progress = st.slider("Progress %",0,100,0)

    target_date = st.date_input("Target Date")

    status = st.selectbox("Status",config_file["Status_List"])

    if st.button("Save Certification"):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            config_file["Saving_Certification_Button_Script"],
            (
                cert_name,
                progress,
                str(target_date),
                status
            )
        )

        conn.commit()
        conn.close()

        st.success("Certification Saved")

        log.info("Certification Saved")

# ---------------------------------------------------
# MONTHLY REVIEW
# ---------------------------------------------------

elif page == "Monthly Review":

    st.header(" Monthly Review")

    if st.button("Generate Monthly Review"):

        review = generate_monthly_review()

        st.write(review)

        log.info("Monthly Review Generated")

# ---------------------------------------------------
# AI COACH
# ---------------------------------------------------

elif page == "AI Coach":

    st.header(" AI Coach")

    if st.button("Start Coach Mode"):

        conn = get_connection()
        cursor = conn.cursor()

        try:

            advice = get_ai_coaching(cursor)

            st.write(advice)

            log.info("AI Coach Response Displayed")

        finally:

            conn.close()