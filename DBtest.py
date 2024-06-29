from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import pymysql

conf ={
    'host' : "sql12.freemysqlhosting.net",
    'port' : '3306',
    'user' : 'sql12713553',
    'password' : 'HlXAIRZVFy',
    'database' : 'sql12713553',
}




if __name__ == '__main__':
 
    try:
        # GET THE CONNECTION OBJECT (ENGINE) FOR THE DATABASE
        connection_string = ("mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}".format(**conf))
        engine = create_engine(connection_string)
        print("Connection to the {host} for user {user} created successfully.".format(**conf))
    except Exception as ex:
        print("Connection could not be made due to the following error: \n", ex)

#create table
metadataObj = MetaData()

# metadataObj.create_all(engine)
# print(metadataObj)

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
