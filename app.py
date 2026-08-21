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

/* Main App Background (Soft Cream/Sepia) */
.stApp {
    background-color: #faf6ee;
    color: #1c1917; /* Dark charcoal text for maximum readability */
}

/* Headers (Fixed: Swapped from white to dark charcoal) */
h1, h2, h3, [data-testid="stHeader"] {
    color: #1c1917 !important;
}

/* Sidebar (Maintained clean, deep navy dark mode) */
section[data-testid="stSidebar"] {
    background-color: #1e293b !important;
    border-right: 1px solid #334155;
}

/* Target all text metrics inside the main block to be dark */
[data-testid="stMainBlockContainer"] p, 
[data-testid="stMainBlockContainer"] label, 
[data-testid="stMainBlockContainer"] span,
[data-testid="stMetricValue"] div,
[data-testid="stMetricLabel"] div {
    color: #1c1917 !important;
}

/* Sidebar Specific Text (Kept light for the dark background) */
section[data-testid="stSidebar"] p, 
section[data-testid="stSidebar"] label, 
section[data-testid="stSidebar"] span, 
section[data-testid="stSidebar"] div {
    color: #e2e8f0 !important;
}

/* Interactive Element Dropdowns in Main Area (Fixed contrast) */
[data-testid="stMainBlockContainer"] .stSelectbox div,
[data-testid="stMainBlockContainer"] .stSelectbox span {
    color: #1c1917 !important;
}

/* Buttons */
.stButton button {
    background-color: #3b82f6;
    color: white !important;
    border-radius: 10px;
    border: none;
    padding: 0.6rem 1rem;
    font-weight: 600;
}

.stButton button:hover {
    background-color: #2563eb;
}

/* Input Fields (Ensured inputs match the text requirements of their containers) */
[data-testid="stMainBlockContainer"] .stTextInput input,
[data-testid="stMainBlockContainer"] .stTextArea textarea {
    background-color: #ffffff;
    color: #1c1917 !important;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
}

section[data-testid="stSidebar"] .stTextInput input,
section[data-testid="stSidebar"] .stTextArea textarea {
    background-color: #0f172a;
    color: #ffffff !important;
    border: 1px solid #334155;
    border-radius: 8px;
}

/* Selectbox Formatting */
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

if page == "Dashboard":
    st.header("Dashboard")
    conn = get_connection()
    cursor = conn.cursor()
    total_logs = cursor.execute(config_file["Dashboard_Daily_Logs_Script"]).fetchone()[0]
    total_learnings = cursor.execute(config_file["Learning_track_Logs_Script"]).fetchone()[0]
    total_certifications = cursor.execute(config_file["Certificate_Logs_Script"]).fetchone()[0]
    avg_productivity = cursor.execute("""SELECT AVG(productivity)FROM daily_logs""").fetchone()[0]

    if avg_productivity is None:
        avg_productivity = 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Daily Logs",total_logs)
    col2.metric("Learnings",total_learnings)
    col3.metric("Certifications",total_certifications)
    col4.metric("Avg Productivity",round(avg_productivity, 2))

    st.subheader("Productivity Trend")
    productivity_df = pd.read_sql_query(config_file["Productivity_Trend_Script"],conn)

    if not productivity_df.empty:
        st.line_chart(productivity_df.set_index("log_date"))


    st.subheader(" Learning Categories")
    learning_df = pd.read_sql_query(config_file["learning_tracker_category_count_Script"],conn)
    
    if learning_df.empty:
        st.info("No learning records available.")
    else:
        st.bar_chart(learning_df.set_index("category"))



    st.subheader(" Certification Progress")
    cert_df = pd.read_sql_query(config_file["certification_Dashboard_Script"],conn)
    if cert_df.empty:
        st.info("No Certification records available.")

    else:
        st.dataframe(cert_df)

        for _, row in cert_df.iterrows():
            st.write(row["Certification_name"])
            st.progress(int(row["progress"]) / 100)
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

