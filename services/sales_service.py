from database.connection import Database
from datetime import datetime 
import sqlite3
from models.sale import Sale

class SalesService:
    def __init__(self,db_instance):
        self.db = db_instance

    def create_sale(self, doc, amount, user,sale_date=None):
        try:
            if sale_date:
                new_timestamp = datetime.combine(sale_date, datetime.now().time()).isoformat()
            else:
                new_timestamp = datetime.now().isoformat()

                
            new_sale = """ 
            INSERT INTO sales (doc, amount, timestamp, user_id)
            VALUES (?, ?, ?, ?)
            """

            values = (doc, amount, new_timestamp, user.id)

            self.db.con.execute(new_sale,values)
            self.db.con.commit()
            return True
        except sqlite3.IntegrityError:
            print("Error db")
            return False
        except Exception as e:
            self.db.con.rollback()
            print(f"Error {e}")
            return False


    
    def get_sales_by_user(self, user):
        try:
            get_sales = """ 
                SELECT * FROM sales WHERE user_id =? ORDER BY timestamp DESC
            """

            cursor = self.db.con.cursor()

            cursor.execute(get_sales,(user.id,))

            rows = cursor.fetchall()

            if not rows :
                print("Error no data")
                return []
            sales = []
            for row in rows:
                sale = Sale(
                    id=row[0],
                    doc=row[1],
                    amount=row[2],
                    timestamp=row[3],
                    user_id=row[4]
                )
                sales.append(sale)
            return sales
        except Exception as e:
            print(f"Error {e}")
            return []

    def get_sales_by_month(self, user,year, month):
        try:
            get_sales = """
            SELECT * FROM sales
            WHERE user_id = ? AND strftime('%Y', timestamp) = ? AND strftime('%m', timestamp) = ? ORDER BY timestamp DESC
        """

            cursor = self.db.con.cursor()

            cursor.execute(get_sales, (user.id, str(year), f'{month:02d}'))

            rows = cursor.fetchall()

            if not rows :
                print("Error no data")
                return []
            sales = []
            for row in rows:
                sale = Sale(
                    id=row[0],
                    doc=row[1],
                    amount=row[2],
                    timestamp=row[3],
                    user_id=row[4]
                )
                sales.append(sale)
            return sales
        except Exception as e:
            print(f"Error {e}")
            return []

    def get_sales_by_year(self, user, year):

        try:
            get_sales = """
            SELECT * FROM sales
            WHERE user_id = ? AND strftime('%Y', timestamp) = ? ORDER BY timestamp DESC
        """

            cursor = self.db.con.cursor()

            cursor.execute(get_sales, (user.id, str(year)))

            rows = cursor.fetchall()

            if not rows :
                print("Error no data")
                return []
            sales = []
            for row in rows:
                sale = Sale(
                    id=row[0],
                    doc=row[1],
                    amount=row[2],
                    timestamp=row[3],
                    user_id=row[4]
                )
                sales.append(sale)
            return sales
        except Exception as e:
            print(f"Error {e}")
            return []
        

    def get_sales_by_date(self, user, date):
        
        try:
            get_sales = """
            SELECT * FROM sales
            WHERE user_id = ? AND date(timestamp) = ?
            ORDER BY timestamp DESC
        """

            cursor = self.db.con.cursor()

            cursor.execute(get_sales, (user.id, date.isoformat()))

            rows = cursor.fetchall()

            if not rows :
                print("Error no data")
                return []
            sales = []
            for row in rows:
                sale = Sale(
                    id=row[0],
                    doc=row[1],
                    amount=row[2],
                    timestamp=row[3],
                    user_id=row[4]
                )
                sales.append(sale)
            return sales
        except Exception as e:
            print(f"Error {e}")
            return []
    

    def delete_sale(self,id):
        if not id:
            print("Error no data")
            return False
        
        try:
            del_com = """DELETE FROM sales WHERE id =?"""
            cursor = self.db.con.cursor()
            cursor.execute(del_com,(id,))
            self.db.con.commit()
            return True
        except Exception as e:
            self.db.con.rollback()
            print(f"Error no data: {e}")
            return False