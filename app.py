# app.py

import logging as log
import os

import pandas as pd
import streamlit as st

from datetime import date,timedelta
from dotenv import load_dotenv
from Agents.database import get_style, get_config, get_connection, get_prompt, get_user_details
from Agents.ai_helper import ask_ai
from Agents.ai_coach import get_ai_coaching
from Agents.review_generator import get_weekly_summary
from Agents.monthly_review import generate_monthly_review

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

config_file = get_config()
Pages = config_file["Pages"]
st.set_page_config(page_title=os.getenv("App_Name", "GrowthMate"),layout="wide")

st.markdown(f"<style>{get_style()}</style>",unsafe_allow_html=True)

if "app_started" not in st.session_state:
    log.info("Application Launched Successfully")
    st.session_state.app_started = True

st.title(os.getenv("App_Name", "GrowthMate"))
st.sidebar.markdown("""
#  GrowthMate
### AI Learning & Career Assistant
---
""")
page = st.sidebar.selectbox(
    "Select Module",
    list(Pages.values())
)

if page == Pages["dashboard"]:
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

# ---------------------------------------------------
# DAILY REVIEW
# ---------------------------------------------------

if page == Pages["daily_review"]:

    st.header("Daily Review")
    st.caption(
        "Capture accomplishments, learnings, blockers and plans for tomorrow."
    )

    # Initialize Session State

    default_values = {
        "accomplishments": "",
        "learnings": "",
        "blockers": "",
        "plan": "",
        "productivity": 5
    }

    for key, value in default_values.items():

        if key not in st.session_state:
            st.session_state[key] = value

    # Form

    with st.form("daily_review_form", clear_on_submit=True):

        accomplishments = st.text_area(
            "What did you accomplish today?",
            key="accomplishments",
            height=120
        )

        learnings = st.text_area(
            "What did you learn today?",
            key="learnings",
            height=120
        )

        blockers = st.text_area(
            "Any blockers?",
            key="blockers",
            height=100
        )

        plan = st.text_area(
            "Tomorrow's Plan",
            key="plan",
            height=120
        )

        productivity = st.slider(
            "Productivity Score",
            min_value=1,
            max_value=10,
            key="productivity"
        )

        submitted = st.form_submit_button(
            "Save Daily Review",
            use_container_width=True
        )

    if submitted:

        missing_fields = []

        if not accomplishments.strip():
            missing_fields.append("Accomplishments")

        if not learnings.strip():
            missing_fields.append("Learnings")

        if not plan.strip():
            missing_fields.append("Tomorrow's Plan")

        if missing_fields:

            st.error(
                f"Please complete the following fields: "
                f"{', '.join(missing_fields)}"
            )

        else:

            try:

                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute(
                    config_file["Save_Daily_review_Script"],
                    (
                        str(date.today()),
                        accomplishments.strip(),
                        learnings.strip(),
                        blockers.strip(),
                        plan.strip(),
                        productivity
                    )
                )

                conn.commit()
                conn.close()

                log.info("Daily Review Saved")

                st.success(
                    "✅ Daily Review saved successfully."
                )

                # Clear Form Values

                st.session_state.accomplishments = ""
                st.session_state.learnings = ""
                st.session_state.blockers = ""
                st.session_state.plan = ""
                st.session_state.productivity = 5

                st.rerun()

            except Exception as ex:

                log.error(
                    "Error saving daily review: %s",
                    ex
                )

                st.error(
                    "Unable to save Daily Review. Please try again."
                )
# ---------------------------------------------------
# LEARNING TRACKER
# ---------------------------------------------------

elif page == Pages["learning_tracker"]:

    st.header(" Learning Tracker")

    learning_date = st.date_input("Learning Date",value=date.today(),
                                  min_value=date.today()- timedelta(days=1),label_visibility="visible")

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

        st.success(learning+" - Learning was Saved Successfully")
        log.info("Learning Saved")

# ---------------------------------------------------
# WEEKLY REVIEW
# ---------------------------------------------------

elif page == Pages["weekly_review"]:

    st.header(" Weekly Review")

    if st.button("Generate Weekly Review"):
        log.info("Weekly Summary Function was Called from App.py")
        weekly_data = get_weekly_summary()
        prompt = get_prompt("weekly_review",data = get_user_details() +"\n"+ weekly_data)
        st.write(ask_ai(prompt))
        if not weekly_data:
            log.error("Approching AI & Weekly Report was causing Mapping Issue")
        else :
            log.info("Weekly Review Generated")

# ---------------------------------------------------
# VIEW HISTORY
# ---------------------------------------------------

elif page == Pages["view_history"]:

    st.header(" View History")

    conn = get_connection()

    data = pd.read_sql_query(config_file["View_History_Script"], conn)
    conn.close()

    if data.empty:
        log.error(Pages["view_history"]+" Data and Script was facing Issue")
    else:
        st.dataframe(data)
        log.info("View History Loaded Successfully")

# ---------------------------------------------------
# CERTIFICATION TRACKER
# ---------------------------------------------------

elif page == Pages["certification_tracker"]:
    st.header(" Certification Tracker")
    cert_name = st.text_input("Certification Name")

    progress = st.slider("Progress %",0,100,0)

    target_date = st.date_input("Target Date",value=date.today() + timedelta(days=90),
                                min_value=date.today(),
                                max_value=date.today() + timedelta(days=365))

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

elif page == Pages["monthly_review"]:
    st.header(" Monthly Review")

    if st.button("Generate Monthly Review"):
        st.write(generate_monthly_review())
        log.info("Monthly Review Generated")

# ---------------------------------------------------
# AI COACH
# ---------------------------------------------------

elif page == Pages["ai_coach"]:
    st.header(" AI Coach")

    if st.button("Start Coach Mode"):
        try:
            st.write(get_ai_coaching())
            log.info("AI Coach Response Displayed")

        finally:
            log.info("AI Coach Enhanced")

st.sidebar.markdown("""
### V1.2.26
---
""")