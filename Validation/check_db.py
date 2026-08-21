
import sqlite3

connection = sqlite3.connect("logs.db")
convalue = connection.cursor()

rows = convalue.execute(
"""SELECT * FROM daily_logs"""
).fetchall()

print("Rows Coun",len(rows))
print(rows)

convalue.close()