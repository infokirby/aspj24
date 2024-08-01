from customer_login import securityQuestions
from wtforms import Form, validators, SelectField, RadioField, BooleanField, StringField, PasswordField, IntegerField, HiddenField
from customer_login import securityQuestions
from wtforms import Form, validators, SelectField, RadioField, BooleanField, StringField, PasswordField, IntegerField, DateField, EmailField, TextAreaField, DateTimeField
from datetime import datetime
from flask_wtf.file import FileAllowed, FileField

class RegistrationForm(Form):
    name = StringField('Name:', [validators.InputRequired()])
    phoneNumber = IntegerField('Phone Number:', [validators.InputRequired(), validators.NumberRange(6000000, 99999999)])
    password = PasswordField('New Password:',[validators.InputRequired(), validators.Regexp(r'\A(?=\S*?\d)(?=\S*?[A-Z])(?=\S*?[a-z])\S{6,}\Z', message="Password must have at least: \n-6 Characters\n-1 Uppercase, \n-1 Number")])
    confirm = PasswordField('Repeat Password:',[validators.InputRequired(), validators.EqualTo('password', message='Passwords must match')])
    gender = SelectField('Gender:', [validators.InputRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male'), ('O', "Other")], default='')
    securityQuestion = SelectField('Security Question:', [validators.InputRequired()], choices=[(1, securityQuestions[1]), (2, securityQuestions[2]),(3, securityQuestions[3]),(4, securityQuestions[4])])
    securityAnswer = StringField('Answer to security question:', [validators.InputRequired()])
    profilePicture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])

class LoginForm(Form):
    phoneNumber = IntegerField('Phone Number:', [validators.InputRequired(), validators.NumberRange(6000000, 99999999)])
    password = PasswordField('Password:', [validators.InputRequired()])
    remember = BooleanField('Remember me:', default=True)

class CustOrderForm(Form):
    phoneNumber = HiddenField()
    datetime = HiddenField()
    stallName = HiddenField()
    orderID = HiddenField()
    item = HiddenField()
    #ingredient = BooleanField('Include Ingredient')
    #ingredientQuantity = IntegerField('Quantity:', [validators.optional(), validators.NumberRange(1, 10)], default=0)
    itemQuantity = IntegerField('Quantity:', [validators.InputRequired(), validators.NumberRange(1, 10)], default=1)
    price = HiddenField()
    total = HiddenField()
    remarks = StringField('Remarks:')
    status = HiddenField(default='Pending')



class EditUserForm(Form):
    name = StringField('Name:', [validators.InputRequired()])
    phoneNumber = IntegerField('Phone Number:', [validators.InputRequired(), validators.NumberRange(6000000, 99999999)])
    gender = SelectField('Gender:', [validators.InputRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male'), ('O', "Other")], default='')
    profilePicture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    
class ChangePasswordForm(Form):
    password = PasswordField('Current Password:',[validators.InputRequired(), validators.Regexp(r'\A(?=\S*?\d)(?=\S*?[A-Z])(?=\S*?[a-z])\S{6,}\Z', message="Password must have at least: \n-6 Characters\n-1 Uppercase, \n-1 Number")])
    newPassword = PasswordField('New Password:',[validators.InputRequired(), validators.Regexp(r'\A(?=\S*?\d)(?=\S*?[A-Z])(?=\S*?[a-z])\S{6,}\Z', message="Password must have at least: \n-6 Characters\n-1 Uppercase, \n-1 Number")])
    confirm = PasswordField('Repeat Password:',[validators.InputRequired(), validators.EqualTo('newPassword', message='Passwords must match')])

class ForgotPasswordForm(Form):
    phoneNumber = IntegerField('Phone Number:', [validators.InputRequired(), validators.NumberRange(6000000, 99999999)])
    securityAnswer = StringField('Answer to security question:', [validators.InputRequired()])
    newPassword = PasswordField('New Password:',[validators.InputRequired(), validators.Regexp(r'\A(?=\S*?\d)(?=\S*?[A-Z])(?=\S*?[a-z])\S{6,}\Z', message="Password must have at least: \n-6 Characters\n-1 Uppercase, \n-1 Number")])
    confirm = PasswordField('Repeat Password:',[validators.InputRequired(), validators.EqualTo('newPassword', message='Passwords must match')])
    
# class OrderForm(Form):
#     food = SelectField('Food', [validators.DataRequired()], choices=[('', 'Select'), ('Plain Waffle', 'Plain Waffle'), ('Chocolate Waffle', 'Chocolate Waffle'), ('Peanut Butter Waffle', 'Peanut Butter Waffle')], default='')
#     quantity = IntegerField('Quantity', [validators.number_range(min=1), validators.DataRequired()])
#     #order_time = DateTimeField('Order Time', format='%m/%d/%y')
#     remarks = TextAreaField('Remarks', [validators.Optional()])
#     order_time = DateTimeField('Order Time', default=datetime.now, format='%Y-%m-%d %H:%M:%S')

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


# class CustOrderForm(Form):
#     phoneNumber = HiddenField()
#     stall = HiddenField()
#     orderID = HiddenField()
#     item = HiddenField()
#     #ingredient = BooleanField('Include Ingredient')
#     #ingredientQuantity = IntegerField('Quantity:', [validators.optional(), validators.NumberRange(1, 10)], default=0)
#     itemQuantity = IntegerField('Quantity:', [validators.InputRequired(), validators.NumberRange(1, 10)], default=1)
#     price = HiddenField()
#     total = HiddenField()
#     remarks = StringField('Remarks:')
#     status = HiddenField(default='Pending')

# class CustOrderFormBBT(Form):
#     phoneNumber = HiddenField()
#     stall = HiddenField()
#     orderID = HiddenField()
#     item = HiddenField()
#     sugarLevel = SelectField('Sugar Level:', [validators.InputRequired()], choices=[(1, '0%'), (2, '25%'),(3, '50%'),(4, '75%'),(5, '100%')], default='')
#     ingredient = HiddenField()
#     ingredientQuantity = IntegerField('Quantity:')
#     itemQuantity = IntegerField('Quantity:', [validators.InputRequired()])
#     price = HiddenField()
#     total = HiddenField()
#     remarks = StringField('Remarks:')
#     status = HiddenField(default='Pending')
