import mysql.connector
from mysql.connector import Error

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

# Replace these variables with your MySQL Workbench connection details
host_name = "127.0.0.1"
user_name = "root"
user_password = "darshan253"
db_name = "eduschema"

connection = create_connection(host_name, user_name, user_password, db_name)

if connection:
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    for table in cursor.fetchall():
        print(table)
    cursor.close()
    connection.close()
