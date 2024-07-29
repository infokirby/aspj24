class StoreOwner:
    def __init__(self, profilePicture = 'default.jpg'):
        self.__profilePicture = profilePicture

    def set_storeName(self, storeName):
        self.__storeName = str(storeName)

    def set_name(self, name):
        self.__name = name

    def set_phoneNumber(self, phoneNumber):
        self.__phoneNumber = phoneNumber

    def set_password(self, password):
        self.__password = password

    def set_profilePicture(self, profilePicture):
        self.__profilePicture = profilePicture

    def get_profilePicture(self):
        return self.__profilePicture

    def get_storeName(self):
        return self.__storeName
    
    def get_id(self):
        return self.__storeName
    
    def get_name(self):
        return self.__name
    
    def get_phoneNumber(self):
        return self.__phoneNumber
    
    def get_password(self):
        return self.__password
    
    def is_active(self):
        return True

    def is_anonymous(self):
        return False
    
    def is_authenticated(self):
        return True
    
#__str__ function
    def __str__(self):
        return f"Store Owner {self.get_storeName()} with phone number {self.get_phoneNumber()}"

