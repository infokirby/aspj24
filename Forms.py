from customer_login import securityQuestions
from flask_wtf import FlaskForm, RecaptchaField
from customer_login import securityQuestions
from wtforms import Form, validators, SelectField, RadioField, BooleanField, StringField, PasswordField, IntegerField, DateField, EmailField, TextAreaField, DateTimeField, HiddenField
from wtforms.validators import InputRequired, NumberRange, Regexp, EqualTo
from datetime import datetime
from badPwValidator import is_not_weak_password
from flask_wtf.file import FileAllowed, FileField


class RegistrationForm(Form):
    name = StringField('Name:', [validators.InputRequired()])
    phoneNumber = IntegerField('Phone Number:', [validators.InputRequired(), validators.NumberRange(6000000, 99999999)])
    password = PasswordField('New Password:',[validators.InputRequired(), validators.Regexp(r'\A(?=\S*?\d)(?=\S*?[A-Z])(?=\S*?[a-z])\S{6,}\Z', message="Password must have at least: \n-6 Characters\n-1 Uppercase, \n-1 Number"), is_not_weak_password])
    confirm = PasswordField('Repeat Password:',[validators.InputRequired(), validators.EqualTo('password', message='Passwords must match')])
    profilePicture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])


class LoginForm(Form):
    phoneNumber = IntegerField('Phone Number:', [validators.InputRequired(), validators.NumberRange(6000000, 99999999)])
    password = PasswordField('Password:', [validators.InputRequired()])
    remember = BooleanField('Remember me:', default=True)

class CustOrderForm(FlaskForm):
    recaptcha = RecaptchaField()
    phoneNumber = HiddenField()
    orderDatetime = HiddenField(default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    stallName = HiddenField()
    orderID = HiddenField()
    item = HiddenField()
    itemQuantity = IntegerField('Quantity:', default=1)
    price = HiddenField()
    total = HiddenField()
    remarks = StringField('Remarks:', default='No Remarks')
    status = HiddenField(default='Pending')



class EditUserForm(Form):
    name = StringField('Name:', [validators.InputRequired()])
    phoneNumber = IntegerField('Phone Number:', [validators.InputRequired(), validators.NumberRange(6000000, 99999999)])
    profilePicture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    
class ChangePasswordForm(Form):
    password = PasswordField('Current Password:',[validators.InputRequired(), validators.Regexp(r'\A(?=\S*?\d)(?=\S*?[A-Z])(?=\S*?[a-z])\S{6,}\Z', message="Password must have at least: \n-6 Characters\n-1 Uppercase, \n-1 Number")])
    newPassword = PasswordField('New Password:',[validators.InputRequired(), validators.Regexp(r'\A(?=\S*?\d)(?=\S*?[A-Z])(?=\S*?[a-z])\S{6,}\Z', message="Password must have at least: \n-6 Characters\n-1 Uppercase, \n-1 Number"), is_not_weak_password])
    confirm = PasswordField('Repeat Password:',[validators.InputRequired(), validators.EqualTo('newPassword', message='Passwords must match')])

class ForgotPasswordForm(Form):
    phoneNumber = IntegerField('Phone Number:', [validators.InputRequired(), validators.NumberRange(6000000, 99999999)])
    securityAnswer = StringField('Answer to security question:', [validators.InputRequired()])
    newPassword = PasswordField('New Password:',[validators.InputRequired(), validators.Regexp(r'\A(?=\S*?\d)(?=\S*?[A-Z])(?=\S*?[a-z])\S{6,}\Z', message="Password must have at least: \n-6 Characters\n-1 Uppercase, \n-1 Number"), is_not_weak_password])
    confirm = PasswordField('Repeat Password:',[validators.InputRequired(), validators.EqualTo('newPassword', message='Passwords must match')])
    

class StoreOwnerRegistrationForm(Form):
    storeName = StringField('Store Name:', [validators.InputRequired()])
    name = StringField('Name:', [validators.InputRequired()])
    phoneNumber = IntegerField('Phone Number:', [validators.InputRequired(), validators.NumberRange(6000000, 99999999)])
    password = PasswordField('New Password:',[validators.InputRequired(), validators.Regexp(r'\A(?=\S*?\d)(?=\S*?[A-Z])(?=\S*?[a-z])\S{6,}\Z', message="Password must have at least: \n-6 Characters\n-1 Uppercase, \n-1 Number")])
    confirm = PasswordField('Repeat Password:',[validators.InputRequired(), validators.EqualTo('password', message='Passwords must match')])

class StoreOwnerLoginForm(Form):
    phoneNumber = IntegerField('Phone Number:', [validators.InputRequired(), validators.NumberRange(6000000, 99999999)])
    password = PasswordField('Password:', [validators.InputRequired()])
    remember = BooleanField('Remember me:', default=True)


