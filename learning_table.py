import sqlite3
import json
import logging as log
connection = sqlite3.connect("logs.db")
connections = connection.cursor()
Config_Filename = "config.json"


with open(Config_Filename, "r") as file:
        config_file = json.load(file)

connections.execute(config_file["Learning_table_Script"])
connection.commit()
connection.close()
log.info("Learning Table Created")