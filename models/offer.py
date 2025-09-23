
from datetime import datetime

class Offer :
    def __init__(self,id,cif,name,address,phone,timestamp,user_id, products=None):
        self.id = id
        self.cif = cif
        self.name = name
        self.address = address
        self.phone = phone
        self.timestamp = timestamp
        self.user_id = user_id
        self.products = products if products is not None else []
    
    def get_formatted_time(self):
        dt_object = datetime.fromisoformat(self.timestamp)
        return dt_object.strftime('%H:%M')