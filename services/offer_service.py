from database.connection import Database
from datetime import datetime, date 
import sqlite3
from models.user import User

class OfferService:
    def __init__(self,db_instance):
        self.db = db_instance

    def create_offer(self, cif, products, user):
        try:
            if not products:
                self.db.con.rollback()
                print("Products list is empty → Offer not created")
                return False

            cursor = self.db.con.cursor()
            new_timestamp = datetime.now().isoformat()
            new_offer = """ 
            INSERT INTO offers (cif, timestamp, user_id)
            VALUES (?, ?, ?)
            """

            values = (cif, new_timestamp, user.id)

            cursor.execute(new_offer,values)
            
            offer_id = cursor.lastrowid


            new_offer_positions = """ 
            INSERT INTO offers_positions (offer_id, product_code, product_name, quantity, unit_price, vat)
            VALUES (?, ?, ?, ?, ?, ?)
            """

            for product in products:
                values = (
                    offer_id,
                    product.get('product_code'), 
                    product.get('product_name'), 
                    product.get('quantity'), 
                    product.get('unit_price'), 
                    product.get('vat')
                )
                cursor.execute(new_offer_positions,values)
           
            self.db.con.commit()
            print("Offer Created")
            return True
            

        except sqlite3.IntegrityError:
            self.db.con.rollback()
            print("Error db")
            return False
        except Exception as e:
            self.db.con.rollback()
            print(f"Error {e}")
            return False


    
    def get_offers_by_user(self, user):
        try:
            get_offers = """ 
                SELECT * FROM offers WHERE user_id =? ORDER BY timestamp DESC
            """

            cursor = self.db.con.cursor()

            cursor.execute(get_offers,(user.id,))

            offers = cursor.fetchall()

            if not offers :
                print("Error no data")
                return []

            final_offers = []
            for offer in offers:
                offer_dict = {
                    'id': offer[0],
                    'cif': offer[1],
                    'timestamp': offer[2],
                    'user_id': offer[3]
                }
                get_positions_sql = """
                    SELECT product_code, product_name, quantity, unit_price, vat 
                    FROM offers_positions 
                    WHERE offer_id = ?
                """
                cursor.execute(get_positions_sql, (offer[0],))
                positions_data = cursor.fetchall()
                
                offer_dict['products'] = [
                    {'product_code': p[0], 'product_name': p[1], 'quantity': p[2], 'unit_price': p[3], 'vat': p[4]}
                    for p in positions_data
                ]
                
                final_offers.append(offer_dict)

            
            print("Fetched Offers")
            return final_offers
        except Exception as e:
            print(f"Error {e}")
            return []
        