from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import CreateSchema
from sqlalchemy.orm import relationship, sessionmaker
from flask_login import UserMixin
from sqlalchemy.engine import URL

url_object = URL.create(
    "mysql+pymysql",
    username="root",
    password="mysqlpassword",
    host="localhost",
    database="customer",
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
    twoFA = Column(Boolean(), nullable=True)
    roles = relationship('Role', secondary=roles_users, backref='customers')


    #Mutators
    def set_password(self, password):
        self.password = password

    def set_name(self, name):
        self.name = name

    def set_id(self, id):
        self.phoneNumber = id

    #Accessors
    def get_id(self):
        return self.phoneNumber

    def get_name(self):
        return self.name

    #Flask_login requirements
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def is_authenticated(self):
        return True



# Create table in database for storing roles
class Role(Base):
    __tablename__ = 'role'
    ID = Column(Integer(), primary_key=True)
    roleName = Column(String(80), unique=True)

# # Create the tables in the database
# metadata.create_all(engine)

# Initialize the database with some data (optional)
def init_db():
    super_role = Role(roleName='superUser')
    session.add(super_role)
    session.commit()

    admin_user = Customer(phoneNumber=90288065, name='Lucian', twoFA=False)
    admin_user.hashedPW = 'Password'  # Note: Normally you'd hash the password
    admin_user.roles.append(super_role)
    session.add(admin_user)
    session.commit()

if __name__ == '__main__':
    init_db()
