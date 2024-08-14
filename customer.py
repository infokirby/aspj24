#import User

class Customer():
    def __init__(self, phoneNumber):
        self.__phoneNumber = str(phoneNumber)

    # accessor methods
    def get_customer_id(self):
        return self.__customer_id
    
    @property
    def get_datetime(self):
        return self.__datetime

    @property
    def get_stallName(self):
        return self.__stallName
    
    @property
    def get_orderID(self):
        return self.__orderID
    
    @property
    def get_item(self):
        return self.__item
    
    @property
    def get_itemQuantity(self):
        return self.__itemQuantity
    
    @property
    def get_ingredient(self):
        return self.__ingredient
    
    @property
    def get_ingredientQuantity(self):
        return self.__ingredientQuantity
    
    @property
    def get_price(self):
        return self.__price
    
    @property
    def get_total(self):
        return self.__total
    
    @property
    def get_remarks(self):
        return self.__remarks
    
    @property
    def get_status(self):
        return self.__status
    
    def get_name(self):
        return self.__name
    
    def get_id(self):
        return str(self.__phoneNumber)
    
    def get_email(self):
        return self.__email
    
    def get_password(self):
        return self.__password
    
    def get_gender(self):
        return self.__gender
    
    def get_membership(self):
        return self.__membership
    
    def get_securityQuestion(self):
        return self.__securityQuestion
    
    def get_securityAnswer(self):
        return self.__securityAnswer

    # mutator methods
    def set_customer_id(self, customer_id):
        self.__customer_id = customer_id

    # def set_food(self, food):
    #     self.__food = food

    # def set_quantity(self, quantity):
    #     self.__quantity = quantity

    # def set_remark(self, remark):
    #     self.__remark = remark

    # def set_order_time(self,order_time):
    #     self.__order_time = order_time
        
    def set_datetime(self, datetime):
        self.__datetime = datetime
        
    def set_stallName(self, stallName):
        self.__stallName = stallName

    def set_orderID(self, orderID):
        self.__orderID = orderID

    def set_item(self, item):
        self.__item = item

    def set_itemQuantity(self, itemQuantity):
        self.__itemQuantity = itemQuantity

    def set_ingredient(self, ingredient):
        self.__ingredient = ingredient

    def set_ingredientQuantity(self, ingredientQuantity):
        self.__ingredientQuantity = ingredientQuantity

    def set_price(self, price):
        self.__price = price

    def set_total(self, total):
        self.__total = total

    def set_remarks(self, remarks):
        self.__remarks = remarks

    def set_status(self, status):
        self.__status = status

    def set_name(self, name):
        self.__name = name

    def set_id(self, phoneNumber):
        self.__id = phoneNumber
        
    def set_email(self, email):
        self.__email = email

    def set_password(self, password):
        self.__password = password

    def set_gender(self, gender):
        self.__gender = gender


    def set_membership(self, membership):
        self.__membership = membership

    def set_securityQuestion(self, securityQuestion):
        self.__securityQuestion = securityQuestion

    def set_securityAnswer(self, securityAnswer):
        self.__securityAnswer = securityAnswer    

#Login requirements
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def is_authenticated(self):
        return True

#pfp
    def set_profilePicture(self, profilePicture):
        self.profilePicture = profilePicture

    def get_profilePicture(self):
        return self.profilePicture

#__str__ function
    def __str__(self):
        return f"User {self.get_name()} with phone number {self.get_id()}"