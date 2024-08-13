from customer import Customer as C
from re import compile

class CustomerLogin(C):
    def __init__(self, phoneNumber, password):
        super().__init__(phoneNumber)
        self.set_password(password)

class RegisterAdmin(C):
    def __init__(self, phoneNumber, password, profilePicture = 'default.jpeg'):
        super().__init__(phoneNumber)
        self.set_password(password)
        if profilePicture:
            self.set_profilePicture(profilePicture)

class RegisterCustomer(C):
    def __init__(self, name, phoneNumber, email, password, gender, securityQuestion, securityAnswer, profilePicture = 'default.jpeg'):
        super().__init__(phoneNumber)
        self.set_id(phoneNumber)
        self.set_email(email)
        self.set_password(password)
        self.set_name(name)
        self.set_gender(gender)
        self.set_securityQuestion(securityQuestion)
        self.set_securityAnswer(securityAnswer)
        if profilePicture:
            self.set_profilePicture(profilePicture)

class EditDetails(C):
    def __init__(self, phoneNumber, name, email, gender, profilePicture = 'default.jpeg'):
        super().__init__(phoneNumber)
        self.set_name(name)
        self.set_email(email)
        self.set_gender(gender)
        if profilePicture:
            self.set_profilePicture(profilePicture)

class ChangePassword(C):
    def __init__(self, phoneNumber, password):
        super().__init__(phoneNumber)
        self.set_password(password)




securityQuestions = {
    1 : "What was the first exam you failed?",
    2 : "In what city or town did your parents meet?",
    3 : "What was the name of your first stuffed animal?",
    4 : "How old were you when you lost your first kiss?"
    }





