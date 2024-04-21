from customer import Customer as C
from re import compile

class CustomerLogin(C):
    def __init__(self, phoneNumber, password):
        super().__init__(phoneNumber)
        self.set_password(password)

class RegisterAdmin(C):
    def __init__(self, phoneNumber, password):
        super().__init__(phoneNumber)
        self.set_password(password)

class RegisterCustomer(C):
    def __init__(self, name, phoneNumber, password, gender, securityQuestion, securityAnswer):
        super().__init__(phoneNumber)
        self.set_password(password)
        self.set_name(name)
        self.set_gender(gender)
        self.set_securityQuestion(securityQuestion)
        self.set_securityAnswer(securityAnswer)

class EditDetails(C):
    def __init__(self, phoneNumber, name, gender):
        super().__init__(phoneNumber)
        self.set_name(name)
        self.set_gender(gender)

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





