import sqlite3
import json
import logging as log

connection = sqlite3.connect("logs.db")
conn = connection.cursor()
try:
    with open("config.json","r") as file:
        files = json.load(file)

    conn.execute(files["Certification_table_Script"])
    log.info("Certification Table Executed")
except Exception as ex:
    log.error("Script Issue ", ex)

connection.commit()
connection.close()

log.info("Certification Table Created")
