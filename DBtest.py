import pymysql

host = "database-1.cr0sk8kqijy4.ap-southeast-1.rds.amazonaws.com"
user = 'admin'
password = 'Password@123'
database = 'database-1'

connection = pymysql.connect(host=host, user=user, password=password, database= database)
with connection:
    cur = connection.cursor()
    version = cur.fetchone()
    print("Database version: {} ".format(version[0]))
