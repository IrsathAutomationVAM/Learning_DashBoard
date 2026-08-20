import sqlite3, json
from ai_helper import ask_ai

def generate_monthly_review():

    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()

    with open("config.json","r") as file:
     config_file = json.load(file)

    data = cursor.execute(config_file["Review_Script"]).fetchall()
    conn.close()
    summary = ""
    for row in data:
        summary += f"""Accomplishments:
        {row[0]}

        Learnings:
        {row[1]}

        Blockers:
        {row[2]}

        """

    prompt = f"""
        You are a professional performance coach.

        Generate a Monthly Self Review.

        Activities:

        {summary}

        Include:

        1. Achievements
        2. Learning Activities
        3. Challenges
        4. Growth Areas
        5. Future Goals

        Use professional language.
        """

    return ask_ai(prompt)