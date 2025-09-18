import bcrypt
from database.connection import Database
from models.user import User

class AuthService:
    def __init__(self, db_instance):
        self.db = db_instance

    def register_user(self, username, email, password,is_admin):
        salt = bcrypt.gensalt()
        password_en = password.encode('utf-8')
        password_hash = bcrypt.hashpw(password_en,salt)
        try:
            

            insert_new_user = """ 
            INSERT INTO users (username, email, password_hash, is_admin)
            VALUES(?, ?, ?, ?);
            """

            values = (username, email, password_hash, is_admin)

            self.db.con.execute(insert_new_user,values )
            self.db.con.commit()
            print("User Added")
            return True
        except sqlite3.IntegrityError:
            print("Username already exists")
            return False
        except Exception as e:
            print(f"Error: {e}")
            return False

    def login_user(self, username, password):
        try:
            cursor = self.db.con.cursor()
            new_query = """ 
            SELECT * FROM users WHERE username=? ;
            """ 
            cursor.execute(new_query,(username,))
            user_data = cursor.fetchone()

            if user_data == None:
                return None

            user_id, username_db, email_db, password_hash_db, is_admin_db = user_data

            if bcrypt.checkpw(password.encode('utf-8'),password_hash_db) == True:
                print("User logged in succesfully")
                new_user = User(username_db,email_db, password_hash_db,bool(is_admin_db),user_id )
                return new_user
            else:
                print("Wrong password")
                return None


        except Exception as e:
            print(f"Error: {e}")
            return None


