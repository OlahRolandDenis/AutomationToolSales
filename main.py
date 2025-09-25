import tkinter as tk
from tkinter import ttk, messagebox
from database.connection import Database
from services.auth_service import AuthService
from services.sales_service import SalesService
from services.offer_service import OfferService
from ui.login_window import LoginWindow
from ui.dashboard_window import DashboardWindow


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sales & Offers AgroMagman")
        self.geometry("800x600")
        
        self.withdraw()

        db = Database()
        self.auth_service = AuthService(db)
        self.sales_service = SalesService(db)
        self.offer_service = OfferService(db)

        self.current_user = None

        self.show_login_window()  
         
    def show_login_window(self):
        self.log_win = LoginWindow(auth_service = self.auth_service, on_login_success = self.on_login_success)


    def on_login_success(self,user):
        self.user = user
        self.show_dashboard_window()

    def show_dashboard_window(self):
        self.dsh_win = DashboardWindow(user = self.user, sales_service = self.sales_service, offer_service= self.offer_service )


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
