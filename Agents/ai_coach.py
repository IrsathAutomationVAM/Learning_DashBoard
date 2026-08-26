# ai_coach.py
import logging as log
from Agents.database import get_config, get_connection, get_prompt
from Agents.database import get_user_details
from Agents.ai_helper import ask_ai


def get_ai_coaching():

    try:
        conn = get_connection()
        cursor = conn.cursor()
        log.info("AI Coach Connected with DB")
        config_file=get_config()
        query = (config_file["Review_Script"]+ " ORDER BY id DESC LIMIT 20")
        logs = cursor.execute(query).fetchall()
        log.info("Rows Retrieved: %s", len(logs))

        if not logs:
            return "No activity logs found."

        summary = ""
        for row in logs:
            summary += f"""
                        Accomplishments:
                        {row[0]}

                        Learnings:
                        {row[1]}

                        Blockers:
                        {row[2]}
                        """

        prompt = get_prompt("ai_coach",data=get_user_details()+"\n"+summary)

        log.info("Sending prompt to OpenRouter")
        response = ask_ai(prompt)
        log.info("AI Coach Response Received")

        return response

    except Exception as ex:
        log.error("AI Coach Error: %s", ex)
        return f"AI Coach Error: {ex}"