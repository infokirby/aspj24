from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import pymysql

conf ={
    'host' : "database-1.cr0sk8kqijy4.ap-southeast-1.rds.amazonaws.com",
    'port' : '3306',
    'user' : 'admin',
    'password' : 'Password123',
    'database' : 'database-1',
}

connection_string = ("mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}".format(**conf))
engine = create_engine(connection_string)

#create table
metadataObj = MetaData()

metadataObj.create_all(engine)
print(metadataObj)

# user_table = Table(
#     "Users",
#     metadataObj,
#     Column("phoneNo", Integer, primary_key=True),
#     Column("name", String(50)),
# )

# connection = pymysql.connect(host=host, user=user, password=password, database= database)
# with connection:
#     cur = connection.cursor()
#     version = cur.fetchone()
#     print("Database version: {} ".format(version[0]))
