
from datetime import datetime

class Offer :
    def __init__(self,id,cif,timestamp,user_id):
        self.id = id
        self.cif = cif
        self.timestamp = timestamp
        self.user_id = user_id
    
    def get_formatted_time(self):
        dt_object = datetime.fromisoformat(self.timestamp)
        return dt_object.strftime('%H:%M')