import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sqlite3
import json

conn = sqlite3.connect("logs.db")
cursor = conn.cursor()

with open("config.json", "r") as file:
        config_file = json.load(file)

tables = cursor.execute(config_file["Table_View_Script"]).fetchall()

print("Tables:" ,'\n',"="*20)

for table in tables:
    print(table[0])

conn.close()