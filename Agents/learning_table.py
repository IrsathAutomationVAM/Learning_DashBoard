import logging as log
from database import get_config,get_connection

connection = get_connection()
connections = connection.cursor()

config_file = get_config()

connections.execute(config_file["Learning_table_Script"])
connection.commit()
connection.close()
log.info("Learning Table Created")