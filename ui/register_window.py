import customtkinter as ctk
from tkinter import messagebox

class RegistrationWindow(ctk.CTk):
    def __init__(self, auth_service, parent_window, on_registration_success=None):
        super().__init__()
        self.parent_window = parent_window
        self.auth_service = auth_service
        self.on_registration_success = on_registration_success
        self.title("Register")
        self.geometry("400x350")
        self.configure(fg_color="#ffffff")
        self.create_widgets()
    
    def create_widgets(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(expand=True)
        
        self.username_entry = ctk.CTkEntry(
            master=frame, 
            placeholder_text="Username",
            width=200, height=35,
            fg_color="#fafafa",
            text_color="#2b2a2a"
        )
        self.username_entry.pack(pady=10)
        
        
        self.password_entry = ctk.CTkEntry(
            master=frame, 
            placeholder_text="Password", 
            show="*",
            width=200, height=35,
            fg_color="#fafafa",
            text_color="#2b2a2a"
        )
        self.password_entry.pack(pady=10)
        
        self.confirm_password_entry = ctk.CTkEntry(
            master=frame, 
            placeholder_text="Confirm Password", 
            show="*",
            width=200, height=35,
            fg_color="#fafafa",
            text_color="#2b2a2a"
        )
        self.confirm_password_entry.pack(pady=10)
        
        
        self.register_button = ctk.CTkButton(
            master=frame, 
            text="Register",
            command=self.handle_register,
            fg_color="#2b2a2a", 
            hover_color="#d7d9dc",
            text_color="#e2e0e0"
        )
        self.register_button.pack(pady=5)
        
        self.back_button = ctk.CTkButton(
            master=frame, 
            text="Back to Login",
            command=self.handle_back,
            fg_color="#2b2a2a", 
            hover_color="#f5f5f5",
            text_color="#e2e0e0"
        )
        self.back_button.pack(pady=5)
    
    def handle_back(self):
        self.parent_window.deiconify()
        self.destroy()

    def handle_register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not username :
            messagebox.showerror("Error", "Please enter username.")
            return
        if not password :
            messagebox.showerror("Error", "Please enter password.")
            return
        if not confirm_password :
            messagebox.showerror("Error", "Please enter confirm password.")
            return
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords doesn't match.")
            return
        
        status = self.auth_service.register_user(username, password, False)

        if status == False:
           
           messagebox.showerror("Error", "Registration failed. Username may already exist.")
        else:
            messagebox.showinfo("Success", "Registration successful! You can now log in.")
            self.destroy()
        
        