from store_owner import StoreOwner as S

class StoreOwnerLogin(S):
    def __init__(self, phoneNumber, password):
        self.set_phoneNumber(phoneNumber)
        self.set_password(password)

class CreateStoreOwner(S):
    def __init__(self, storeName, name, phoneNumber, password):
        self.set_storeName(storeName)
        self.set_name(name)
        self.set_phoneNumber(phoneNumber)
        self.set_password(password)

