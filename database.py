# database.py

import sqlite3
import json

conn = sqlite3.connect("logs.db")
cursor = conn.cursor()

with open("config.json","r") as file:
    config_file = json.load(file)

cursor.execute(config_file["Daily_Logs_Table_Script"])

conn.commit()
conn.close()