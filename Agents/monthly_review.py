from Agents.database import get_config,get_connection,get_prompt,get_user_details
from Agents.ai_helper import ask_ai

def generate_monthly_review():

    conn = get_connection()
    cursor = conn.cursor()

    config_file = get_config()

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

    prompt = get_prompt("monthly_review",data=get_user_details()+"\n"+summary)

    return ask_ai(prompt)
