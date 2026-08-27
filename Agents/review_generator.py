from Agents.database import get_config,get_connection

def get_weekly_summary():

    conn = get_connection()
    cursor = conn.cursor()

    config_file = get_config()
    User_Script = config_file["Review_Script"]+ " ORDER BY id DESC LIMIT 7"
    data = cursor.execute(User_Script).fetchall()

    conn.close()

    summary = ""

    for row in data:
        summary += f"""
                Accomplishments:
                {row[0]}

                Learnings:
                {row[1]}

                Blockers:
                {row[2]}

                -------------------------
                """

    return summary

