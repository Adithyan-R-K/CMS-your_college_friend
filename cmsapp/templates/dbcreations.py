import mysql.connector
conn = mysql.connector.connect(user='root',password='',host='localhost',database='cms_database')
if conn:
    print("connected successfully")
else:
    print("connection not establishesd")