import customtkinter as ctk
from ui.register_window import RegistrationWindow

class LoginWindow(ctk.CTk):
    def __init__(self, auth_service, on_login_success):
        super().__init__()
        self.auth_service = auth_service
        self.on_login_success = on_login_success
        self.title("Main Window")
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
        
        self.password_entry = ctk.CTkEntry(
            master=frame, 
            placeholder_text="password", 
            show="*",
            width=200, height=35,
            fg_color="#fafafa",
            text_color="#2b2a2a"
        )
        self.password_entry.pack(pady=10)
        
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
            password = self.password_entry.get()
            if not username or  not password :
                ctk.CTkMessagebox.showerror("Error", "Please enter both username and password.")
                return
            
            new_user = self.auth_service.login_user(username,password)

            if not new_user:
                ctk.CTkMessagebox.showerror("Login Failed", "Invalid username or password.")
            else:
                print("Login successful")
                self.on_login_success(new_user)
                self.destroy()
    def handle_register(self):
        self.withdraw()
        registration_window = RegistrationWindow(self.auth_service, self)
        registration_window.grab_set()



            



  