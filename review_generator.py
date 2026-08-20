import sqlite3
import json

def get_weekly_summary():

    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()

    with open("config.json", "r") as file:
        config_file = json.load(file)
    User_Script = config_file["Review_Script"]+ " ORDER BY id DESC LIMIT 7"
    print(User_Script)
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


if __name__ == "__main__":
    print(get_weekly_summary())
