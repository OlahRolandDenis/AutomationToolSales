from datetime import datetime

class Sale :
    def __init__(self,id,doc,amount,timestamp,user_id):
        self.id = id
        self.doc = doc
        self.amount = amount
        self.timestamp = timestamp
        self.user_id = user_id
    
    def get_formatted_time(self):
        dt_object = datetime.fromisoformat(self.timestamp)
        return dt_object.strftime('%H:%M')