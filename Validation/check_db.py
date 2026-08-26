import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Agents.database import get_connection

connection = get_connection()
convalue = connection.cursor()

rows = convalue.execute(
"""SELECT * FROM daily_logs"""
).fetchall()

print("Rows Coun",len(rows))
print(rows)

convalue.close()