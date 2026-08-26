import logging as log
from Agents.database import get_config,get_connection

connection = get_connection()
conn = connection.cursor()
try:
    files = get_config()
    conn.execute(files["Certification_table_Script"])
    log.info("Certification Table Executed")

except Exception as ex:
    log.error("Script Issue ", ex)

connection.commit()
connection.close()

log.info("Certification Table Created")
