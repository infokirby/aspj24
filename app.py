#General Libraries
from dotenv import load_dotenv
import shelve, sys, xlsxwriter, base64, json, stripe, webbrowser, re, os, pandas, numpy, requests, logging
from io import BytesIO
from datetime import datetime, timedelta
from flask_talisman import Talisman
from werkzeug.utils import secure_filename
import uuid

#Flask Framework
from flask import Flask, render_template, url_for, request, redirect, flash, session, send_file, jsonify, send_from_directory
from flask_wtf.csrf import CSRFProtect


#For forms rendering
from Forms import RegistrationForm, LoginForm, EditUserForm, ChangePasswordForm, ForgotPasswordForm, StoreOwnerRegistrationForm, CustOrderForm
from customer_login import CustomerLogin, RegisterCustomer, EditDetails, ChangePassword, securityQuestions, RegisterAdmin
from customer_order import CustomerOrder, newOrderID
from customer import Customer
from store_owner import StoreOwner
from store_owner_login import StoreOwnerLogin, CreateStoreOwner
from menu import menu as menu

#For Login Functions
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_bcrypt import Bcrypt
from flask.sessions import SecureCookieSessionInterface
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

#For ML 
import joblib
from logs_config import write_csv_log, orderLog
from iptest import geolocate, get_public_ip
from sklearn.preprocessing import StandardScaler


#For PFP checker
from extensionChecker import ALLOWED_EXTENSIONS, allowed_file

#for database
from flask_sqlalchemy import SQLAlchemy
from DBcreateTables import Customer, Role, Orders
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, URL, Insert, Result, Boolean, text, update
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.schema import CreateSchema

# For logs
from logs_config import orderLog, loginLog, syslog, write_csv_log

GOOGLE_VERIFY_URL = 'https://www.google.com/recaptcha/api/siteverify'





#Login ML load
iso_forest = joblib.load('iso_forest_model.pkl')
scaler = joblib.load('scaler.pkl')
feature_names = ['hour', 'day', 'month', 'year'] + [f'location_{loc}' for loc in ['SG']]


app = Flask(__name__, template_folder='Templates', static_folder='Static')

# csrf protect
csrf = CSRFProtect(app)
csrf.init_app(app)
app.config.update(
    SESSION_COOKIE_SECURE=False,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

csp = {
    'default-src': [
        '\'self\'',
        'cdnjs.cloudflare.com',
        'fonts.googleapis.com',
        'fonts.gstatic.com',
        'use.fontawesome.com',
        'cdn.jsdelivr.net',
        'kit.fontawesome.com',
        'ka-f.fontawesome.com',        
        'www.google.com/recaptcha/',
        'www.recaptcha.net',
    ],
    'img-src': ['\'self\''],
    'style-src': [
        '\'self\'',
        '\'unsafe-inline\'',  
        'fonts.googleapis.com',
        'use.fontawesome.com',
        'cdn.jsdelivr.net',
        'kit.fontawesome.com',
        'www.google.com/recaptcha/',
        'www.recaptcha.net',
    ],
    'font-src': [
        '\'self\'',
        'fonts.gstatic.com',
        'use.fontawesome.com',
        'cdn.jsdelivr.net',
        'kit.fontawesome.com',
        'ka-f.fontawesome.com'  
    ],
    'connect-src': [  
        '\'self\'',
        'ka-f.fontawesome.com'
    ],
    'script-src': [
        '\'self\'',
        '\'unsafe-inline\'',
        'cdn.jsdelivr.net',
        'kit.fontawesome.com',
        'ka-f.fontawesome.com',
        'www.google.com/recaptcha/api.js',
        'www.google.com/recaptcha/',
        'www.recaptcha.net',
        'https://www.gstatic.com/recaptcha/'
    ]
}

Talisman(app, content_security_policy=csp)

load_dotenv()

stripe.api_key = os.getenv("STRIPE_API_KEY")
bcrypt = Bcrypt(app)

#API configs
app.config['SECRET_KEY'] = 'SH#e7:q%0"dZMWd-8u,gQ{i]8J""vsniU+Wy{08yGWDDO8]7dlHuO4]9/PH3/>n'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LdcmxUqAAAAAGVF_1zJ26DFEs61J2oJ8cQ3eM-4' 
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LdcmxUqAAAAAHUKANmhqXNRcY8ZvRjiTl-Uzjmm'
login_manager = LoginManager()
csrf = CSRFProtect(app)

#Session Timeout
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 5)

app.config['UPLOAD_FOLDER'] = 'Static/profile_pics'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB max size for uploads
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:Password123@database-1.cr0sk8kqijy4.ap-southeast-1.rds.amazonaws.com'

stripe.api_key = "sk_test_51OboMaDA20MkhXhqx0KQdxFgKbMYsLGIciIpWAKrwhXhXHytVQkPncx6SPDL79SOW0fdliJpbUkQ01kq5ZDdjYmP00nojJWp0p"
bcrypt = Bcrypt(app)
db = SQLAlchemy()
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
limiter = Limiter(
    get_remote_address, 
    app = app,
    storage_uri = "memory://"
)

#Database Connection things
url_object = URL.create(
    "mysql+pymysql",
    username="admin",
    password="awsPassword123fk",
    host="aspj24-final.cybuljfuqrm3.us-east-1.rds.amazonaws.com",
    database="ASPJ_DB",
)
#DB engine config
engine = create_engine(url_object)
metadata = MetaData(schema="ASPJ_DB")
with engine.connect() as conn:
    if not conn.dialect.has_schema(conn, "ASPJ_DB"): 
        conn.execute(CreateSchema("ASPJ_DB"))
Base = declarative_base(metadata=metadata)
# conn = engine.connect()
Session = sessionmaker(bind=engine)
dbSession = Session()


#configuring flask limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri="memory://"
)

#SuperUser account
hashed_password = bcrypt.generate_password_hash("Pass123").decode('utf-8')
superUser = RegisterAdmin(90288065, hashed_password)

@app.route('/session_data')
def session_data():
    return "Check the console for session data"

#all logs
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


#Creating pfp path if not avil
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.after_request
def apply_caching(response):
    response.headers["Set-Cookie"] = SecureCookieSessionInterface().get_signing_serializer(app).dumps(dict(session))
    response.headers.add('Set-Cookie','SameSite=None; Secure')
    return response
def save_picture(form_picture):
    filename = str(uuid.uuid4()) + '_' + secure_filename(form_picture.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        form_picture.save(filepath)
    except Exception as e:
        pass
    return filename


@login_manager.user_loader
def load_user(id):
    try:
        return dbSession.query(Customer).filter(Customer.phoneNumber == id).first()
    except Exception as e:
        dbSession.rollback()

    finally:
        dbSession.close()
    # with shelve.open('userdb', 'c') as userdb:
    #     if id in userdb:
    #         for keys in userdb:
    #             if keys == id:
    #                 return userdb[id]
            
        # elif id == superUser.get_id():
        #     return superUser

        # else:
        #     with shelve.open('SOdb', 'c') as SOdb:
        #         for keys in SOdb:
        #             if keys == id:
        #                 return SOdb[id]
        


#home page
@app.route('/')
def home():
    return render_template('home.html')

#storeownder home page
@app.route('/storeOwnerHome')
def storeOwnerHome():
    return render_template('storeOwnerHome.html')


@app.route('/admin', methods=['GET', 'POST'])
def adminLogin():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        if form.phoneNumber.data == 90288065:
            admin = RegisterAdmin(69, form.password.data)
            if isinstance(admin, Customer):
                if bcrypt.check_password_hash(superUser.get_password(), form.password.data):
                    login_user(admin)
                    session['id'] = admin.get_id()
                    with shelve.open("userdb", 'c') as userdb:
                        customerCount = len(userdb)
                        return render_template('adminPage.html',  logined = True, customerCount=customerCount)

                else:
                    flash("For Admins only. Unauthorised access forbiddened.", 'Danger')
                    return redirect(url_for('home'))
    return render_template('adminLogin.html', form=form)

# @app.route('/adminPage')
# @login_required
# def adminPage():
#     with shelve.open("userdb", 'c') as userdb:
#         customerCount = len(userdb)
#         return render_template('adminPage.html', customerCount=customerCount)
    


@app.route('/createStoreOwner', methods=['GET', 'POST'])
def createStoreOwner():
    form = StoreOwnerRegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        with shelve.open('SOdb', 'c') as SOdb:
            if str(form.storeName.data) not in SOdb:
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                storeOwner = CreateStoreOwner(form.storeName.data, form.name.data, form.phoneNumber.data, hashed_password)
                if isinstance(storeOwner, StoreOwner):
                    SOdb[storeOwner.get_storeName()] = storeOwner
                    flash('Registration Successful!', "success")
                    return redirect(url_for('login'))
            else:
                flash("Creation unsuccessful" , 'warning')
                return redirect(url_for('createStoreOwner'))
    return render_template('createStoreOwner.html', form=form)

#About us pages
@app.route('/openingHours')
def openingHours():
    return render_template('openingHours.html')

@app.route('/findUs')
def findUs():
    return render_template('findUs.html')

@app.route('/contactUs')
def contactUs():
    return render_template('contactUs.html')


#Login Page
@app.route('/login', methods=['GET', 'POST'])
# @limiter.limit("15/hour;5/minute")
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            user = dbSession.query(Customer).filter(Customer.phoneNumber == form.phoneNumber.data).first()
            if isinstance(user, Customer) and bcrypt.check_password_hash(user.hashedPW, form.password.data):
                remember = form.remember.data
                login_user(user, remember=remember)
                session['id'] = int(user.get_id())
                write_csv_log('loginlog.csv', [user.get_id(), geolocate(get_public_ip()), datetime.now().month, datetime.now().day, datetime.now().weekday(), datetime.now().hour, datetime.now().minute])
                return render_template('home.html')
            
            else:
                flash("Wrong Username/Password.\n Please try again", 'danger')

        except Exception as e:
            flash(f"An error {e} occured. Please try again.", "Warning")

        finally:
            dbSession.close()
    return render_template('login.html', form=form)


    #     with shelve.open('userdb', 'c') as userdb:
    #         user = CustomerLogin(form.phoneNumber.data, form.password.data)
    #         if isinstance(user, Customer):
    #             for keys in userdb:
    #                 if user.get_id() == keys:
    #                     if bcrypt.check_password_hash(userdb[keys].get_password(), form.password.data):
    #                          #extract data here
    #                         currentDT = datetime.now().timetuple()
    #                         hour = currentDT[3]
    #                         day = currentDT[2]
    #                         month = currentDT[1]
    #                         year = currentDT[0]

    #                         new_data = pandas.DataFrame({
    #                             'hour': [hour],
    #                             'day' : [day],
    #                             'month' : [month],
    #                             'year' : [year],
    #                         })

    #                         location_dummies = pandas.get_dummies(geolocate('219.74.99.238'), prefix='location')
    #                         for col in location_dummies.columns:
    #                             new_data[col] = location_dummies[col]
    
    #                             # Ensure all location columns are present
    #                             for col in feature_names:
    #                                 if col not in new_data.columns:
    #                                     new_data[col] = 0

    #                         for col in new_data.columns:
    #                             pandas.concat
                            
    #                         # Extract features for prediction
    #                         X_new = new_data[feature_names].values

    #                         # Standardize the features
    #                         X_new_scaled = scaler.transform(X_new)
                            
    #                         # Predict if the login data is an anomaly
    #                         prediction = iso_forest.predict(X_new_scaled)
                                

    #                         if prediction[0] == -1: #anomaly
    #                             flash("Login not authorised. Please leave site.", "danger")
    #                             return render_template('login.html', form=form)
                            
    #                         else:
    #                             if form.remember.data:
    #                                 login_user(userdb[keys], remember=True)
    #                             else:
    #                                 login_user(userdb[keys])
    #                         session['id'] = user.get_id()
    #                         return render_template('home.html', logined=True)
    #         flash("wrong username/password. please try again", "warning")
    #         return redirect(url_for('login'))
    # return render_template('login.html', form=form)


#Registration Route
@app.route('/register', methods=['GET', 'POST'])
@limiter.limit("15/hour;5/minute")
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = dbSession.query(Customer).filter(Customer.phoneNumber == form.phoneNumber.data).first()
        if not user:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

            profile_picture_filename = "default.jpeg"
            if 'profilePicture' in request.files:
                profile_picture_file = request.files['profilePicture']
                if profile_picture_file and profile_picture_file.filename != '':
                    if allowed_file(profile_picture_file.filename):
                        profile_picture_filename = save_picture(profile_picture_file)
                        user.set_profilePicture(profile_picture_filename)
                    else:
                        flash('Allowed file types are - png, jpg, jpeg', 'danger')
                    
            new_user = Customer(phoneNumber = form.phoneNumber.data, name = form.name.data, hashedPW = hashed_password, profilePicture_location = profile_picture_filename)
            role = dbSession.query(Role).filter(Role.roleName == "user").first()
            new_user.roles.append(role)
            if isinstance(new_user, Customer):
                dbSession.add(new_user)
                dbSession.commit()
                session.clear()
                flash('Registration Successful!', "success")
                return redirect(url_for('login'))
        else:
            flash("Already registered please login instead" , 'success')
            return redirect(url_for('login'))
        
    dbSession.close()
    return render_template('register.html', form=form)
    

@app.route('/2fa', methods = ["POST", "GET"])
@limiter.limit("15/hour;5/minute")
def authentication():
    form = Authorisation(request.form)
    if request.method == 'POST' and form.validate():
        with shelve.open('userdb', 'c') as userdb:
            user = CustomerLogin(form.phoneNumber.data, form.password.data)
            if isinstance(user, Customer):
                for keys in userdb:
                    if user.get_id() == keys:
                        if bcrypt.check_password_hash(userdb[keys].get_password(), form.password.data):
                            if form.remember.data == True:
                                login_user(userdb[keys], remember=True)
                            else:
                                login_user(userdb[keys])
                            session['id'] =int(user.get_id())
                            return render_template('home.html', logined = True)

            else:
                flash("wrong username/password. please try again", "warning")
                return redirect(url_for('login'))
    return render_template('login.html', form=form)


#Store Owner Login
@app.route('/storeOwnerLogin', methods=["POST", "GET"])
def storeOwnerLogin():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            storeOwner = dbSession.query(StoreOwner).filter(StoreOwner.phoneNumber == form.phoneNumber.data).first()
            if isinstance(storeOwner, StoreOwner) and bcrypt.check_password_hash(storeOwner.hashedPW, form.password.data):
                remember = form.remember.data
                login_user(storeOwner, remember=remember)
                session['id'] = int(storeOwner.get_id())
                return render_template('storeOwnerHome.html')
            
            else:
                flash("Wrong Username/Password.\n Please try again", 'danger')

        except Exception as e:
            flash("An error occured. Please try again.", "Critical")

        finally:
            dbSession.close()
    return render_template('storeOwnerLogin.html', form=form)

#Forgot Pw
@app.route('/forgotPassword', methods=["Get", "POST"])
def forgotPassword():
        
    secQn = None
    form = ForgotPasswordForm(request.form)
    if request.method == "POST":
        user = Customer(form.phoneNumber.data)
        with shelve.open('userdb', 'c') as userdb:
            for key in userdb:
                if key == user.get_id():
                    
                    secQn = securityQuestions[int(userdb[key].get_securityQuestion())]
                    if form.validate():
                        if userdb[key].get_securityAnswer() == form.securityAnswer.data.strip().title():
                            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') 
                            user = userdb[key]
                            user.set_password(hashed_password)
                            if isinstance(user, Customer):
                                userdb[key] = user
                                flash("Password successfully reset.", "success")
                                return redirect(url_for("login"))
                            
                            else:
                                flash("something went wrong", "warning")
                                return redirect(url_for('forgotPassword'))

                    elif form.securityAnswer.data == None:
                        return render_template("forgotPassword.html", form=form, secQn = secQn)
                    
                    else:
                        flash("Incorrect Security Question Answer", "warning")
                        return redirect(url_for('forgotPassword'))
    return render_template("forgotPassword.html", form=form, secQn = secQn)


#profile page
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = EditUserForm(request.form)
    if request.method == 'POST' and form.validate():
        currentUser = dbSession.query(Customer).filter(Customer.phoneNumber == current_user.get_id()).first()
        if isinstance(currentUser, Customer):
            currentUser.set_name(form.name.data)
            currentUser.set_id(form.phoneNumber.data)
            if 'profilePicture' in request.files:
                profile_picture_file = request.files['profilePicture']
                if profile_picture_file and profile_picture_file.filename != '':
                    if allowed_file(profile_picture_file.filename):
                        profile_picture_filename = save_picture(profile_picture_file)
                        currentUser.set_profilePicture(profile_picture_filename)
                    else:
                        flash('Allowed file types are - png, jpg, jpeg', 'danger')
                        return redirect(url_for('profile'))

            try:
                dbSession.add(currentUser)
                dbSession.commit()
                flash('Successfully edited', 'success')
            except Exception as e:
                dbSession.rollback()
                flash(f'An error occurred: {e}', 'danger')

            dbSession.close()
        return redirect(url_for('profile'))
        
    return render_template('profile.html', form=form)
        
#Upload PFP
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded', 'success')
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


#change password page
@app.route('/changePassword', methods=['GET', 'POST'])
@login_required
def changePassword():
    form = ChangePasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        currentUser = dbSession.query(Customer).filter(Customer.phoneNumber == current_user.get_id()).first()
        new_hashed_password = bcrypt.generate_password_hash(form.newPassword.data).decode('utf-8')
        if bcrypt.check_password_hash(current_user.get_password(), form.password.data):
            if isinstance(currentUser, Customer):
                currentUser.set_password(new_hashed_password)
                try:
                    dbSession.add(currentUser)
                    dbSession.commit()
                    flash('Password successfully edited', 'success')
                except Exception as e:
                    dbSession.rollback()
                    flash(f'An error occurred: {e}', 'danger')

                finally:
                    dbSession.close()
                return redirect(url_for('home'))
        else:
            flash("Password change unsuccessful", "danger")
            return redirect(url_for('changePassword'))

    return render_template('changePassword.html', form=form)


@app.route('/deleteProfile', methods = ["POST", "GET"])
@login_required
def deleteProfile():
    form = request.form
    if request.method == "POST":
        if request.form.get('Delete') == 'Delete':
            try:
                dbSession.delete(dbSession.query(Customer).filter(Customer.phoneNumber == current_user.get_id()).first())
                dbSession.commit()
                flash("Profile deleted. Please register for future use.", "success")


            except Exception as e:
                    dbSession.rollback()
                    flash(f'An error occurred: {e}', 'danger')

            finally:
                dbSession.close()

            session.pop('id')
            logout_user()
            return redirect(url_for('home'))

        elif  request.form.get('Cancel') == 'Cancel':
            flash("Profile deletion aborted", "warning")
            return redirect(url_for('profile'))
        else:
            pass
    elif request.method == 'GET':
        return render_template('deleteProfile.html', form=form)

    return render_template('deleteProfile.html')

def sanitize_input(input_string):
    # This pattern matches any character that is not a word character or a space
    pattern = re.compile(r'[^\w\s]')
    sanitized_string = re.sub(pattern, '', input_string)
    return sanitized_string

# recaptcha verification
def verify_recaptcha(response_token):
    secret_key = '6LdcmxUqAAAAAHUKANmhqXNRcY8ZvRjiTl-Uzjmm'  # Replace with your actual secret key
    url = 'https://www.google.com/recaptcha/api/siteverify'
    data = {
        'secret': secret_key,
        'response': response_token
    }
    response = requests.post(url, data=data)
    result = response.json()
    return result

#order
@app.route('/Vegetarian', methods=['GET', 'POST'])
@app.route('/Muslim', methods=['GET', 'POST'])
@app.route('/Indian', methods=['GET', 'POST'])
@app.route('/Chicken Rice', methods=['GET', 'POST'])
@app.route('/Pizza', methods=['GET', 'POST'])
@app.route('/Japanese', methods=['GET', 'POST'])
@app.route('/Ban Mian', methods=['GET', 'POST'])
@app.route('/Curry Rice', methods=['GET', 'POST'])
@app.route('/Yong Tau Foo', methods=['GET', 'POST'])
@app.route('/Mala', methods=['GET', 'POST'])
@app.route('/Bubble Tea', methods=['GET', 'POST'])
@app.route('/Takoyaki', methods=['GET', 'POST'])
@app.route('/Snack', methods=['GET', 'POST'])
@app.route('/Waffle', methods=['GET', 'POST'])
@app.route('/Drinks', methods=['GET', 'POST'])
@login_required
def stalls():
    path = request.path
    stall_name = path.lstrip('/')
    form = CustOrderForm(request.form)
    now = datetime.now()    

    if request.method == "POST":
        #regex to remove special characters
        if form.remarks.data != "":
            sanitized_remarks = sanitize_input(form.remarks.data)
        # if verification_result.get('success') or not verification_result.get('success'):
        newOrder = Orders(customerID = current_user.get_id(), stallName = stall_name, item = form.item.data, itemQuantity = form.itemQuantity.data, price = form.price.data, total = float(request.form.get('price')) * float(request.form.get('itemQuantity')), remarks = sanitized_remarks)
        if isinstance(newOrder, Orders):
            try:
                dbSession.add(newOrder)
                dbSession.commit()
                flash("Item added to cart!", "success")

            except Exception as e:
                dbSession.rollback()
                flash("Error occured. Please try again", "warning")

        # order create log
        dbSession.close()
        
    
    else:
        print("Form not validated")
        print(form.errors)
        
    return render_template(f'{stall_name}.html', menu=menu, stall_name=stall_name, form=form)



#Cart
@app.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    
    total = 0
    orders = [] 
    form = CustOrderForm(request.form)
    customerOrders = dbSession.query(Orders).filter(Orders.customerID == current_user.get_id()).all()
    for order in customerOrders:
        if order.get_status() == "Pending":
            orders.append(order)
            total = total + order.get_total()


    dbSession.close()
    return render_template('cart.html', menu=menu, orders=orders, form=form, total=f'{total:.2f}')

#mark complete
@app.route('/completeOrder/<string:id>', methods=['GET', 'POST'])
@login_required
def completeOrder(id):
    # order complete log
    currentOrder = dbSession.query(Orders).filter(Orders.ID == id).first()
    currentOrder.set_status_complete()
    logrecord = [currentOrder.customerID, currentOrder.get_datetime(), currentOrder.get_orderID(), currentOrder.get_stallName(), currentOrder.get_item(), currentOrder.get_itemQuantity(), currentOrder.get_price(), currentOrder.get_total(), currentOrder.get_remarks()]
    write_csv_log('orderlog.csv', logrecord)

    try:
        dbSession.add(currentOrder)
        dbSession.commit()
        flash('Moved into order history.', 'success')
    except Exception as e:
        dbSession.rollback()
        flash(f'An error occurred: {e}', 'danger')

    dbSession.close()
    return redirect(url_for('cart'))



#edit
@app.route('/editOrder/<string:id>', methods=["GET", "POST"])
@login_required
def editOrder(id):
    print("moo")
    form = CustOrderForm(request.form)
    print("moo")

    if form.validate():
        print("moo")
        price = 0.0
        for i, j in menu.items():
            for form.item.data in j:
                price = j[form.item.data]
                print(price)
        with shelve.open('order.db', 'c') as orderdb:
            order = orderdb[id]
            order.set_itemQuantity(form.itemQuantity.data)
            order.set_total(order.get_itemQuantity * price)
            print(order.get_itemQuantity)
            print(order.get_total)
            order.set_remarks(form.remarks.data)
            orderdb[id] = order
            orderdb.sync()
    else:
        print(form.errors)

    
    # form=form
    return redirect(url_for('cart', menu=menu, form=form))

#delete
@app.route('/deleteOrder/<string:id>', methods=['GET', 'POST'])
@login_required
def deleteOrder(id):
    # order delete log
    customerOrders = dbSession.query(Orders).filter(Orders.customerID == current_user.get_id()).all()
    for order in customerOrders:
        if order.get_orderID() == id:
            try:
                dbSession.delete(order)
                flash(f"Order {id} successfully deleted", "success")
                dbSession.commit()

            except Exception as e:
                dbSession.rollback()
                flash("Error occured, action aborted", 'warning')

            finally:
                dbSession.close()

    return redirect(url_for('cart'))

# delete all
@app.route('/deleteAllOrder', methods=['GET', 'POST'])
@login_required
def deleteAllOrder():
    count = 0
    customerOrders = dbSession.query(Orders).filter(Orders.customerID == current_user.get_id()).all()
    try:
        for order in customerOrders:
            dbSession.delete(order)
        dbSession.commit()
        flash("All orders successfully deleted", 'success')


    except Exception as e:
        dbSession.rollback()
        flash("Error occured, action aborted", 'warning')

    finally:
        dbSession.close()

    return redirect(url_for('cart'))

#Customer Order History
@app.route('/orderHistory', methods=['GET', 'POST'])
@login_required
def orderHistory():
    orders = []
    monthlyTotal = 0
    current_datetime = datetime.now()
    customerOrders = dbSession.query(Orders).filter(Orders.customerID == current_user.get_id()).all()
    for order in customerOrders:
        if order.get_status() == "Completed":
            orders.append(order)
            if order.get_datetime().month == current_datetime.month:
                monthlyTotal += float(order.get_total())
    return render_template('orderHistory.html', menu=menu, orders=orders, monthlyTotal = f"{monthlyTotal:.2f}")

        


    # with shelve.open('order.db', 'c') as orderdb:
    #     orders = []
    #     count = 0
    #     monthlyTotal = 0
    #     current_datetime = datetime.now()
    #     for order in orderdb:
    #         if orderdb[order].get_id() == current_user.get_id() and orderdb[order].get_status == "Completed":
    #             count += 1
    #             if count > 30:
    #                 orders.append(orderdb[order])
    #                 orders.pop(orders[count-30])
    #             else:
    #                 orders.append(orderdb[order])
                    
    #             if orderdb[order].get_dateTimeData.month ==  current_datetime.month:
    #                 monthlyTotal += float(orderdb[order].get_total)
    # return render_template('orderHistory.html', menu=menu, orders=orders, monthlyTotal = f"{monthlyTotal:.2f}")

#Instead of total impliment a monthly tally

price_id = "price_1ObuyUDA20MkhXhqmqe3Niwb"

def calculate_amount():
    total = 0
    customerOrders = dbSession.query(Orders).filter(Orders.customerID == current_user.get_id()).all()
    for order in customerOrders:
        if order.get_status == "Pending":
            total = total + order.get_total()
            return total

@app.route("/checkout")
@login_required
def payment():
    try:
        amount = calculate_amount()
        customerOrders = dbSession.query(Orders).filter(Orders.customerID == current_user.get_id()).all()
        for order in customerOrders:
            if order.get_status == "Pending":
                order.set_status_purchased()

        
        stripe.Price.modify(
        "price_1ObuyUDA20MkhXhqmqe3Niwb",
        active=True, #change to false
        )

        stripe.Price.create(
        product='prod_PQmX9ciU3SUHVk',
        unit_amount_decimal =amount*100,
        currency="sgd",
        lookup_key="pricing",
        active=True
        )

        stripe.Product.modify(
        "prod_PQmX9ciU3SUHVk",
        default_price="price_1Oj2A3DA20MkhXhq3AHH5RXA",
        
        )

    
    except stripe.error.StripeError as e:
        print(f"Error updating price: {e}")
    webbrowser.open_new_tab("https://buy.stripe.com/test_9AQ8wwfBibLX2Pe28e")
    return redirect(url_for('cart'))



#Logout 
@app.route('/logout')
@login_required
def logout():
    logout_user()
    if 'id' in session:
        session.pop('id')
    session.clear()
    flash("User successfully logged out." , 'success')
    return redirect(url_for("home"))


#StoreOwners side
@app.route('/currentOrders')
def current_orders():
    with shelve.open('order.db', 'c') as orderdb:
        order_list = []
        try:
            for order in orderdb:
                if orderdb[order].get_stallName == current_user.get_storeName() and orderdb[order].get_status == "Pending":
                    order_list.append(orderdb[order])
        except KeyError:
            print('Key Error')

    return render_template('currentOrders.html', count=len(order_list), order_list=order_list, accountTypeSO = True)

#mark Ready to collect
@app.route('/collectOrder/<string:id>', methods=['GET', 'POST'])
@login_required
def collectOrder(id):
    with shelve.open('order.db', 'c') as orderdb:
        order = orderdb[id]
        order.set_status("Ready for Collection")
        orderdb[id] = order
    return render_template(('currentOrders.html'))


#StoreOwners Past Orders
@app.route('/pastOrders', methods=['GET', 'POST'])
@login_required
def storeOwnerPastOrders():
    with shelve.open('order.db', 'c') as orderdb:
        orders = []
        total = 0
        count = 0
        for order in orderdb:
            if orderdb[order].get_stallName == current_user.get_storeName() and orderdb[order].get_status == "Completed":
                count += 1
                orders.append(orderdb[order])
                total += float(orderdb[order].get_total)
    return render_template('storeOwnersPastOrders.html', menu=menu, orders=orders, total = f"{total:.2f}", count = count)

@app.route('/dashboard')
@login_required
def dashboard():
    current_datetime = datetime.now()
    banMian = 0
    dumplings = 0
    tyym = 0
    slicedFish = 0

    with shelve.open('order.db', 'c') as orderdb:
        for order in orderdb:
            if orderdb[order].get_stallName == current_user.get_storeName() and orderdb[order].get_status == "Completed":
                if orderdb[order].get_dateTimeData.month ==  current_datetime.month:
                    if orderdb[order].get_item == "Ban Mian":
                        banMian += 1
                    if orderdb[order].get_item == "Dumplings":
                        dumplings += 1
                    if orderdb[order].get_item == "Tom Yam U Mian":
                        tyym += 1
                    if orderdb[order].get_item == "Fish Slice Soup with Bee Hoon":
                        slicedFish += 1

    return render_template('salesDashboard.html', banMian = banMian, dumplings = dumplings, tyym = tyym, slicedFish = slicedFish)


    # db = shelve.open('history.db', 'r')
    # try:
    #     pie_dict = db['orders']
    # except:
    #     raise 404

    # food_list = ['Plain waffle', 'Chocolate Waffle', 'Peanut Butter Waffle']
    # plain_list = []
    # chocolate_list = []
    # peanut_list = []
    # print(pie_dict)
    # for order in pie_dict:
    #     if 'Plain Waffle' in order:
    #         plain_list.append(order.get_quantity())
    #     elif order.get_food() == 'Chocolate Waffle':
    #         chocolate_list.append(order.get_quantity())
    #     elif order.get_food() == "Peanut Butter Waffle":
    #         peanut_list.append(order.get_quantity())

    # db.close()

    # return render_template('salesDashboard.html', )

@app.route('/download_excel_api')
def downloadExcelApi():
    apiResponse = createApiResponse()
    return apiResponse

def createApiResponse():
    bufferFile = writeBufferExcelFile()
    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    return send_file(bufferFile,mimetype=mimetype)
    return response

def writeBufferExcelFile():
    buffer = BytesIO()
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()

    dataHeader=["ID", "Food", "Quantity","Revenue"]
    headerStyle=workbook.add_format(createHeadStyle())
    worksheet.write_row(0,0,dataHeader,headerStyle)

    history_list = []
    orderDetails = []
    try:
        with shelve.open('order.db', 'r') as orderdb:
            for orderID in orderdb:
                if orderdb[orderID].get_stallName == current_user.get_storeName() and orderdb[orderID].get_status == "Completed":
                    orderDetails = [orderdb[orderID].get_orderID, orderdb[orderID].get_item, orderdb[orderID].get_itemQuantity, orderdb[orderID].get_total]
                    history_list.append(orderDetails)


        '''for rowIndex, order in enumerate(history_list):
            OrderValues = list(order.values())'''
        # format = workbook.add_format(createDataStyle())
        # if len(history_list) % 2 == 1:
        #     format = workbook.add_format(createDataStyle('#e2efd9'))
        # worksheet.write_row(len(history_list) + 1, 0, DataWritten(history_list), format)
        # worksheet.set_column(1, 8, 27)

        for col_num, data in enumerate(dataHeader):
            worksheet.write(0, col_num, data)

        for row_num, row_data in enumerate(history_list):
            for col_num, col_data in enumerate(row_data):
                worksheet.write(row_num, col_num, col_data)

    except KeyError:
        print('Key Error')
    except OSError:
        print('OSError')
    
    workbook.close()
    buffer.seek(0)
    return buffer

def DataWritten(history_list):
    dataToBeWritten = []
    for orders in history_list:
        dataToBeWritten = [
            orders.get_customer_id(),
            orders.get_food(),
            orders.get_quantity(),
            orders.get_remark(),
            orders.get_order_time()
        ]
    
    return dataToBeWritten

def createDataStyle(bgColor='#FFFFFF'):
    dataStyle={
        'border': 1,
        'fg_color': bgColor
    }
    return dataStyle

def createHeadStyle():
    headStyle={
       'border': 1,
       'font_size':'12',
       'bold':True,
        'fg_color': '#00b050'
    }
    return headStyle

#Error handling
@app.errorhandler(401)
def not_authorised(error):
        return render_template('error.html', error_code = 401, message = "Please login to view this page")
    
@app.errorhandler(404)
def not_found(error):
        return render_template('error.html', error_code = 404, message = 'Page not found. Sorry for the inconvinience caused.')

@app.errorhandler(413)
def request_entitiy_too_large(error):
    flash('File is too large. Maximum file size is 5 MB', 'danger')
    return redirect(request.url)

# @app.errorhandler(Exception)
# def handle_exception(error):
#     return render_template('error.html', error_code = 500, message='Unknown error occured, please try again later.')

if __name__ == '__main__':
    app.run(debug = True, ssl_context='adhoc')