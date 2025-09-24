class User :
    def __init__(self,username,password_hash,is_admin,id = None):
        self.username = username
        self.password_hash = password_hash
        self.id = id
        self.is_admin = is_admin
    

    def can_view_sale(self):
        return self.is_admin



