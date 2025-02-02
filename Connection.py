import mysql.connector

# Connection Establish
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    port="3306",
    password="root",
    database="dashboard_db",
)
if conn.is_connected():
    print("Connected to MySQL database")


# Cursor Object For Interaction
cursor = conn.cursor()
