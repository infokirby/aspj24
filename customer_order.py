from customer import Customer as C
import shelve

def newOrderID():
    with shelve.open('orderID') as db:
        if 'orderID' not in db:
            db['orderID'] = 0
        db['orderID'] += 1
        return db['orderID']

class CustomerOrder(C):
    def init(self, phoneNumber, stall, orderID, item, itemQuantity, price, total, remarks, status):
        super().__init__()
        self.__stall = stall
        self.__orderID = orderID
        self.__item = item
        self.__itemQuantity = itemQuantity
        #self.__ingredient = ingredient
        #self.__ingredientQuantity = ingredientQuantity
        self.__price = price
        self.__total = total
        self.__remarks = remarks
        self.__status = status

    @property
    def get_stall(self):
        return self.__stall
    
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
    
    @property
    def get_dateTimeData(self):
        return self.__dateTimeData
    
    
    def set_stall(self, stall):
        self.__stall = stall

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

    def set_dateTimeData(self, dateTimeData):
        self.__dateTimeData = dateTimeData

    def __str__(self):
        return f"{self.get_orderID()},{self.get_id()},{self.get_stall()},{self.get_item()},{self.get_itemQuantity()},{self.get_price()},{self.get_total()},{self.get_remarks()},{self.get_status()}"