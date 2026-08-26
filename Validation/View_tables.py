import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Agents.database import get_connection,get_config

conn = get_connection()
cursor = conn.cursor()


config_file = get_config

tables = cursor.execute(config_file["Table_View_Script"]).fetchall()

print("Tables:" ,'\n',"="*20)

for table in tables:
    print(table[0])

conn.close()