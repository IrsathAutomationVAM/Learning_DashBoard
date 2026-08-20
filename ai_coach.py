# ai_coach.py

import json
import logging as log

from ai_helper import ask_ai

def get_ai_coaching(cursor):

    try:

        log.info("AI Coach Connected with DB")

        with open("config.json", "r") as file:
            config_file = json.load(file)

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

        prompt = f"""You are Irsath's personal AI mentor.
                    Analyze the following history:
                    {summary}
                    Provide:
                    1. Strengths
                    2. Weaknesses
                    3. Skill Gaps
                    4. Learning Recommendations
                    5. Certification Recommendations
                    6. Career Guidance for a Software Testing Engineer
                    
                    Use professional language.
                    """

        log.info("Sending prompt to OpenRouter")
        response = ask_ai(prompt)
        log.info("AI Coach Response Received")

        return response

    except Exception as ex:
        log.error("AI Coach Error: %s", ex)
        return f"AI Coach Error: {ex}"