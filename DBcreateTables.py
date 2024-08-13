from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, ForeignKey, Float, DateTime, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import CreateSchema
from sqlalchemy.orm import relationship, sessionmaker
from flask_login import UserMixin
from sqlalchemy.engine import URL
from datetime import datetime as dt

url_object = URL.create(
    "mysql+pymysql",
    username="admin",
    password="awsPassword123fk",
    host="aspj24-final.cybuljfuqrm3.us-east-1.rds.amazonaws.com",
    database="ASPJ_DB",
)

engine = create_engine(url_object)
metadata = MetaData(schema="ASPJ_DB")
with engine.connect() as conn:
    if not conn.dialect.has_schema(conn, "ASPJ_DB"): 
        conn.execute(CreateSchema("ASPJ_DB"))
Base = declarative_base(metadata=metadata)



Session = sessionmaker(bind=engine)
session = Session()

# Association table for the many-to-many relationship between users and roles
roles_users = Table('roles_users', metadata,
    Column('user_id', Integer(), ForeignKey('customer.phoneNumber')),
    Column('role_id', Integer(), ForeignKey('role.ID'))
)

# Create table in database for storing users
class Customer(Base, UserMixin):
    __tablename__ = 'customer'
    phoneNumber = Column(Integer(), unique=True, primary_key=True)
    name = Column(String(255), nullable=False)
    hashedPW = Column(String(255), nullable=False, server_default=" ")
    profilePicture_location = Column(String(255), default='default.jpeg')
    twoFA = Column(Boolean(), nullable=True)
    roles = relationship('Role', secondary=roles_users, backref='customers')
    active = Column(Boolean(), default = True)
    orders = relationship('Orders', back_populates='customer')


    #Mutators
    def set_password(self, password):
        self.hashedPW = password

    def set_name(self, name):
        self.name = name

    def set_id(self, id):
        self.phoneNumber = id

    def lockout(self):
        self.active = False

    def set_profilePicture(self, profilePicture):
        self.profilePicture_location = profilePicture

    #Accessors
    def get_id(self):
        return self.phoneNumber
    
    def get_password(self):
        return self.hashedPW

    def get_name(self):
        return self.name
    
    def get_profilePicture(self):
        return self.profilePicture_location

    #Flask_login requirements
    def is_active(self):
        return self.active
    
    def is_anonymous(self):
        return False
    
    def is_authenticated(self):
        return True

class Orders(Base):
    __tablename__ = 'orders'
    ID = Column(Integer(), primary_key=True, autoincrement=True)
    customerID = Column(Integer(), ForeignKey('customer.phoneNumber'))
    stallName = Column(String(255))
    item = Column(String(255))
    itemQuantity = Column(Integer())
    price = Column(Float())
    total = Column(Float())
    remarks = Column(String(255))
    completionStatus = Column(String(30), default='Pending')
    dateTime = Column(DateTime, default = dt.now())
    customer = relationship('Customer', back_populates='orders')

    def set_status_purchased(self):
        self.completionStatus = 'Purchased'

    def set_status_complete(self):
        self.completionStatus = 'Completed'

    def get_orderID(self):
        return self.ID

    def get_status(self):
        return self.completionStatus
    
    def get_total(self):
        return self.total

    def get_price(self):
        return self.price
    
    def get_item(self):
        return self.item
    
    def get_itemQuantity(self):
        return self.itemQuantity
    
    def get_remarks(self):
        return self.remarks
    
    def get_datetime(self):
        return self.dateTime
    
    def get_stallName(self):
        return self.stallName

# Create table in database for storing roles
class Role(Base):
    __tablename__ = 'role'
    ID = Column(Integer(), primary_key=True)
    roleName = Column(String(80), unique=True)

# # Wipe and update the tables in the database
def wipe():
    metadata.drop_all(engine)
    metadata.create_all(engine)
    adminRole = Role(ID = 1, roleName = "Admin")
    StoreOwner = Role(ID = 2, roleName = 'StoreOwner')
    userRole = Role(ID = 3, roleName = "User")
    session.add(userRole)
    session.add(StoreOwner)
    session.add(adminRole)
    session.commit()
    session.close()

