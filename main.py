from database.connection import Database
from services.auth_service import AuthService
from services.sales_service import SalesService
from services.offer_service import OfferService
from ui.login_window import LoginWindow


"""     def show_login_window(self):
        self.withdraw()
        self.login_window = LoginWindow(auth_service = self.auth_service, on_login_success = self.on_login_success)
        #log_win.mainloop()


    def on_login_success(self,user):
        self.user = user
        if self.login_window:
            self.login_window.destroy()
        self.deiconify()
        self.show_dashboard_window()


    def show_dashboard_window(self):
        dsh_win = DashboardWindow(user = self.user, sales_service = self.sales_service, offer_service= self.offer_service )
        #dsh_win.mainloop() """


if __name__ == "__main__":
    db = Database()
    auth_service = AuthService(db)
    sales_service = SalesService(db)
    offer_service = OfferService(db)
    app = LoginWindow(
        auth_service=auth_service,
        sales_service=sales_service,
        offer_service=offer_service
    )
    app.mainloop()
