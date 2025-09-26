import customtkinter as ctk
from ui.register_window import RegistrationWindow
from tkinter import messagebox
from ui.dashboard_window import DashboardWindow

class LoginWindow(ctk.CTk):
    def __init__(self, auth_service, sales_service, offer_service):
        super().__init__()
        self.auth_service = auth_service
        self.sales_service = sales_service
        self.offer_service = offer_service
        self.title("Login")
        self.geometry("400x250")
        self.configure(fg_color="#ffffff")
        self.create_widgets()
    
    def create_widgets(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(expand=True)
        
        self.username_entry = ctk.CTkEntry(
            master=frame, 
            placeholder_text="username",
            width=200, height=35,
            fg_color="#fafafa",
            text_color="#2b2a2a"
        )
        self.username_entry.pack(pady=10)
        
        
        self.login_button = ctk.CTkButton(
            master=frame, 
            text="Login",
            command=self.handle_login,
            fg_color="#2b2a2a", 
            hover_color="#d7d9dc",
            text_color="#e2e0e0"
        )
        self.login_button.pack(pady=5)
        
        self.register_button = ctk.CTkButton(
            master=frame, 
            text="Register",
            command=self.handle_register,
            fg_color="#2b2a2a", 
            hover_color="#f5f5f5",
            text_color="#e2e0e0"
        )
        self.register_button.pack(pady=5)

    def handle_login(self):

            username = self.username_entry.get()
            
            if not username:
                messagebox.showerror("Error", "Please enter both username.")
                return
            
            new_user = self.auth_service.login_user(username)

            if not new_user:
                messagebox.showerror("Login Failed", "Invalid username.")
            else:
                print("Login successful")
                self.destroy()
                DashboardWindow(
                    user=new_user,
                    sales_service=self.sales_service,
                    offer_service=self.offer_service
                ).mainloop()

    def handle_register(self):
        self.destroy()
        RegistrationWindow(
            auth_service=self.auth_service,
            sales_service=self.sales_service,
            offer_service=self.offer_service
        ).mainloop()



            



  