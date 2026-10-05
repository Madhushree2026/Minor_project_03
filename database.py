import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Madhu@2123",
    database="redflag"
)

if connection.is_connected():
    print("Successfully connected to RedFlag database!")

connection.close()